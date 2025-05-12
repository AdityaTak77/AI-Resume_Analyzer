import streamlit as st
from backend.pdf_ingestion import load_split_pdf
from backend.vector_store import create_vector_store
from backend.analysis import analyze_resume
import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def save_analysis_as_pdf(analysis_text, output_filename):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter  # default page size is letter
    c.setFont("Helvetica", 10)

    # Set up the y position to start writing
    y_position = height - 40

    # Split analysis text into lines and draw each line
    for line in analysis_text.split('\n'):
        if y_position < 40:  # Check if we need to create a new page
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position = height - 40
        c.drawString(40, y_position, line)
        y_position -= 12  # Move down for the next line

    # Save the PDF
    c.save()

# Main application including "Upload Resume" and "Resume Analysis" sections
def render_main_app():
    
    # Apply custom CSS to adjust the sidebar width
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            min-width: 25%;
            max-width: 25%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Moving the upload section to the sidebar
    with st.sidebar:
        st.header("Resume Upload & Job Details")  # Header for the upload section
        
        # File uploader for PDF resumes
        resume_file = st.file_uploader("Upload Your Resume (PDF format)", type="pdf")

        # Text area for job description input
        job_description = st.text_area("Paste Job Description", height=300,help="Copy and paste the complete job description here")

        if resume_file and job_description:  # Check if both inputs are provided
            # Create a temporary directory if it doesn't exist
            temp_dir = "temp"
            os.makedirs(temp_dir, exist_ok=True)

            # Save the uploaded file to the temporary directory
            with open(os.path.join(temp_dir, resume_file.name), "wb") as f:
                f.write(resume_file.getbuffer())
            
            # Load and split the PDF file into documents and chunks
            resume_file_path = os.path.join("temp", resume_file.name)
            resume_docs, resume_chunks = load_split_pdf(resume_file_path)

            # Create a vector store from the resume chunks
            vector_store = create_vector_store(resume_chunks)
            st.session_state.vector_store = vector_store  # Store vector store in session state
                
            # Remove the temporary directory and its contents
            shutil.rmtree(temp_dir)

            # Button to begin resume analysis
            if st.button("Analyze Resume", help="Click to begin the analysis process"):
                # Combine all document contents into one text string for analysis
                full_resume = " ".join([doc.page_content for doc in resume_docs])
                # Analyze the resume
                analysis = analyze_resume(full_resume, job_description)
                # Store analysis in session state
                st.session_state.analysis = analysis    
        else:
            st.info("📌 Please upload your resume and provide the job description to begin the analysis.")

    # Display the analysis result if it exists in session state 
    if "analysis" in st.session_state:
        st.header("Resume Analysis Results")
        st.write(st.session_state.analysis)
        # Save analysis to PDF
        pdf_filename = "analysis_report.pdf"
        save_analysis_as_pdf(st.session_state.analysis, pdf_filename)
        
        # Provide download button for the PDF analysis report
        with open(pdf_filename, "rb") as file:
            st.download_button(
                label="Download Analysis Report (PDF)",
                data=file,
                file_name=pdf_filename,
                mime="application/pdf"
            )
    else:
        st.header("🎯 Smart Resume Analyzer")
        st.subheader("Your one-stop solution for resume screening and analysis.")
        st.info("""
        Get detailed analysis of how well your resume matches the job requirements. 
        Our tool helps you:
        
        1. **Evaluate Resume-Job Fit**: Upload your resume and see how well it matches the position
        2. **Identify Gaps**: Understand what skills or experiences you might need to highlight
        3. **Improve Applications**: Get actionable insights to enhance your resume
        
        Ready to start? Follow these simple steps:
        """)

        todo = ["📄 Upload your resume in PDF format", "📝 Paste the complete job description", "🔍 Click 'Analyze Resume' to get detailed insights"]
        st.markdown("\n".join([f"##### {i+1}. {item}" for i, item in enumerate(todo)]))