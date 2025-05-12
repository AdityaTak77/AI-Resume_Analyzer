import streamlit as st
from frontend.main_app import render_main_app
from frontend.chat_interface import render_chat_interface
from frontend.resume_ranker import render_resume_ranker
from frontend.job_recommender import render_job_recommender
from frontend.job_scraper import render_job_scraper
from frontend.about_us import render_about_us
import os
from dotenv import load_dotenv

# Set the page layout to wide for better visual presentation
st.set_page_config(layout="wide", page_title="Resume Analyzer")
st.image("resume_analyzer.jpeg", width=150)

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Function to handle admin login
def admin_login():
    """Admin login page"""
    st.title("Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state["admin_logged_in"] = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password. Please try again.")

def main():
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ("Resume Screener", "Resume Ranker (Admin)", "Job Recommender", "Job Scraper", "About Us")
    )

    if not st.session_state["admin_logged_in"]:
        if page == "Resume Ranker (Admin)":
            admin_login()
            return  
    else:
        if page == "Resume Ranker (Admin)":
            st.title("Admin Panel - Resume Ranker")
            render_resume_ranker()

    # Page Routing
    if page == "Resume Screener":
        st.title("Resume Screener")
        col1, col2 = st.columns([3, 2])
        with col1:
            render_main_app()
        with col2:
            render_chat_interface()
    
    elif page == "Job Recommender":
        render_job_recommender()

    elif page == "Job Scraper":
        render_job_scraper()
    
    elif page == "About Us":
        render_about_us()

# Initialize session state for admin login if not already set
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# Script execution through the 'main' function
if __name__ == "__main__":
    main()
