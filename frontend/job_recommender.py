import os
import streamlit as st
import PyPDF2 as pdf
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def input_pdf_text(uploaded_file):
    """
    Extract text from a PDF resume.
    
    Args:
        uploaded_file (UploadedFile): The uploaded PDF file.
    
    Returns:
        str: Extracted text from the PDF.
    """
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += str(page.extract_text())
        return text
    except Exception as e:
        st.error(f"Error extracting PDF text: {e}")
        return ""

def generate_sample_skills_data(skills):
    """
    Generate sample skills proficiency data.
    
    Args:
        skills (list): List of skills extracted from resume.
    
    Returns:
        pandas.DataFrame: DataFrame with skills and proficiency levels.
    """
    np.random.seed(42)
    skills_data = pd.DataFrame({
        'Skill': skills,
        'Proficiency': np.random.randint(50, 100, size=len(skills))
    }).sort_values('Proficiency', ascending=False)
    
    return skills_data

def get_job_recommendations(resume_text):
    """
    Generate job recommendations based on the resume content.
    
    Args:
        resume_text (str): Text extracted from the resume.
    
    Returns:
        dict: Recommendations and extracted skills.
    """
    try:
        prompt = f"""
        Analyze the following resume and provide:
        1. Top 5 job title recommendations
        2. Top 10 skills extracted from the resume
        
        Resume: {resume_text}
        """
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        # Parse the response (this is a simplified parsing)
        recommendations = response.text.strip().split('\n')
        
        # Extract job titles and skills
        job_titles = [rec for rec in recommendations if rec.startswith(('1.', '2.', '3.', '4.', '5.'))]
        skills = [rec for rec in recommendations if rec.startswith(('Skill', 'skill'))]
        
        return {
            'job_titles': job_titles,
            'skills': [skill.split(':')[-1].strip() for skill in skills]
        }
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return {
            'job_titles': ['Unable to generate recommendations'],
            'skills': []
        }

def render_job_recommender():
    """
    Render the job recommender page in Streamlit.
    """
    # # Page Configuration
    # st.set_page_config(
    #     page_title="AI Career Navigator", 
    #     page_icon="🚀", 
    #     layout="wide"
    # )
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 30px;
    }
    .sub-header {
        color: #34495E;
        border-bottom: 2px solid #3498DB;
        padding-bottom: 10px;
    }
    .stButton>button {
        background-color: #3498DB;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main Title
    st.markdown('<h1 class="main-title">🚀 AI Career Navigator</h1>', unsafe_allow_html=True)
    
    # Resume Upload Section
    st.markdown('<h2 class="sub-header">Upload Your Resume</h2>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose a PDF file", 
        type=["pdf"], 
        help="Upload your resume in PDF format"
    )
    
    # Job Recommendation Process
    if uploaded_file is not None:
        # Success Notification
        st.success("Resume uploaded successfully! 📄")
        
        # Extract text from the resume
        resume_text = input_pdf_text(uploaded_file)
        
        # Recommendation Button
        if st.button("Discover Your Career Path", type="primary"):
            with st.spinner("Analyzing your potential..."):
                # Get job recommendations
                result = get_job_recommendations(resume_text)
                
                # Create two columns for visualizations
                col1, col2 = st.columns(2)
                
                # Column 1: Job Recommendations
                with col1:
                    st.markdown('<h3 class="sub-header">🎯 Recommended Career Paths</h3>', unsafe_allow_html=True)
                    for title in result['job_titles']:
                        st.markdown(f"- {title}")
                
                # Column 2: Skills Visualization
                with col2:
                    if result['skills']:
                        # Generate sample skills data
                        skills_data = generate_sample_skills_data(result['skills'])
                        
                        # Create a horizontal bar chart of skills
                        fig = px.bar(
                            skills_data, 
                            x='Proficiency', 
                            y='Skill', 
                            orientation='h',
                            title='Your Skills Proficiency',
                            labels={'Proficiency': 'Skill Level', 'Skill': 'Skills'},
                            color='Proficiency',
                            color_continuous_scale='viridis'
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                
                # Detailed Analysis Section
                st.markdown('<h3 class="sub-header">📊 Detailed Career Insights</h3>', unsafe_allow_html=True)
                
                # Career Path Probability Visualization
                career_paths = result['job_titles'][:5]
                probabilities = np.random.dirichlet(np.ones(len(career_paths)), size=1)[0] * 100
                
                career_prob_df = pd.DataFrame({
                    'Career Path': career_paths,
                    'Probability (%)': probabilities
                })
                
                fig_pie = px.pie(
                    career_prob_df, 
                    values='Probability (%)', 
                    names='Career Path',
                    title='Career Path Probability Distribution',
                    hole=0.3
                )
                fig_pie.update_layout(
                    height=600,  # Increase the height
                    width=800,   # Adjust the width
                    margin=dict(t=50, b=50, l=50, r=50)  # Set margins
                )
                
                st.plotly_chart(fig_pie, use_container_width=True)
