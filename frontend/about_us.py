import streamlit as st

def render_about_us():
    """Renders the About Us page with detailed information and visual elements."""
    # Page title
    st.title("About Us")
    
    # Introduction
    st.markdown("""
    Welcome to **Resume Analyzer**, your one-stop solution for intelligent resume screening, ranking, and job recommendation. 
    Our platform leverages the power of advanced AI to streamline recruitment processes and provide insights for both job seekers and employers.
    """)

    # Features Section
    st.subheader("What We Offer")
    st.markdown("""
    Our application includes:
    - **Resume Screener**: Analyze resumes to match job descriptions using AI.
    - **Resume Ranker**: Rank resumes for hiring managers to identify top candidates quickly.
    - **Job Recommender**: Suggest job opportunities tailored to candidates' skills and experiences.
    """)

    # Mission Section
    st.subheader("Our Mission")
    st.markdown("""
    We aim to revolutionize recruitment by:
    - Reducing bias in hiring decisions.
    - Enhancing job seekers' chances with personalized recommendations.
    - Making resume screening and ranking faster and more accurate.
    """)

    # Image (Optional)
    st.image(
        "https://via.placeholder.com/800x400.png?text=Transforming+Recruitment+with+AI",
        caption="Empowering both employers and job seekers.",
        use_container_width=True
    )

    # Contact Section
    st.subheader("Get in Touch")
    st.markdown("""
    We'd love to hear from you! Whether you have feedback, questions, or partnership ideas, feel free to reach out:
    - **Email**: adityatak7733@gmail.com
    - **GitHub**: [View our repository](https://github.com/AdityaTak77/AdityaTak77)
    - **LinkedIn**: [Follow us on LinkedIn](https://www.linkedin.com/in/adityatak7733/)
    """)

    # Footer
    st.markdown("""
    ---
    **Made with ❤️ and AI/LLM by Aditya Tak**
    """)
