import streamlit as st
import base64
import os
import pandas as pd
import PyPDF2 as pdf
import google.generativeai as genai
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    """Generate response using Gemini model."""
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf_text(uploaded_file):
    """Extract text from uploaded PDF."""
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

def render_resume_ranker():
    """Renders the Resume Ranker page with enhanced UI and visualization."""
    # Custom CSS for styling
    st.markdown("""
    <style>
    .main-header {
        color: #2C3E50;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background-color: #F0F4F8;
        border-radius: 10px;
    }
    .subheader {
        color: #34495E;
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #3498DB;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2980B9;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header with custom styling
    st.markdown('<h1 class="main-header">🤖 AI-Powered Resume Screening System</h1>', unsafe_allow_html=True)

    # Prompts for Gemini AI
    prompt_name = """
    Your task is to extract the full name of the candidate from the resume and just return the name. Name of candidate is always given in resume and possibly in the top part of the resume.
    """

    prompt_review = """
    You are an expert ATS system, and your task is to review the resume of the candidate based on the job description provided.
    Provide an overview of the match between the resume and the job description. It should be short and crisp just for the HR to know about the candidate.
    """

    prompt_match_percentage = """
    As an ATS scanner, your task is to calculate the percentage match between the resume and the provided job description.
    Give me the percentage, while calculating percentage keep in mind the skills and the work experience should be taken into consideration in the calculation. That should be according to the job description provided.
    Just give the percentage match value nothing else. Give the score by calculating so that no one can question it.
    """

    # Job Description Input
    input_text = st.text_area("📝 Enter Job Description", key="input", height=200)

    # PDF Upload
    uploaded_files = st.file_uploader("📂 Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)

    # Submit Button
    submit = st.button("🔍 Evaluate Resumes")

    # Processing and Results
    if submit:
        if uploaded_files is not None and len(uploaded_files) > 0:
            results = []
            
            # Process each uploaded resume
            for uploaded_file in uploaded_files:
                pdf_content = input_pdf_text(uploaded_file)
                
                # Get Gemini AI responses
                name_response = get_gemini_response(prompt_name, pdf_content, input_text)
                review_response = get_gemini_response(prompt_review, pdf_content, input_text)
                match_response = get_gemini_response(prompt_match_percentage, pdf_content, input_text)
                
                # Process match percentage
                match_percentage = round(float(match_response.strip().replace('%', '')), 2)
                results.append({
                    'Name': name_response,
                    'Resume Review': review_response,
                    'Percentage Match': match_percentage
                })
            
            # Create DataFrame and rank
            df = pd.DataFrame(results)
            df = df.sort_values(by='Percentage Match', ascending=False)
            df['Ranking'] = df['Percentage Match'].rank(method='first', ascending=False).astype(int)
            
            # Display Results Table
            st.markdown('<h2 class="subheader">📊 Evaluation Results</h2>', unsafe_allow_html=True)
            st.table(df[['Name', 'Resume Review', 'Percentage Match', 'Ranking']])
            
            # Create bar chart of match percentages
            fig = px.bar(
                df, 
                x='Name', 
                y='Percentage Match', 
                title='Resume Match Percentages',
                labels={'Percentage Match': 'Match Percentage'},
                color='Percentage Match',
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig)
            
        else:
            st.warning("Please upload resumes to evaluate.")

def main():
    render_resume_ranker()

if __name__ == "_main_":
    main()