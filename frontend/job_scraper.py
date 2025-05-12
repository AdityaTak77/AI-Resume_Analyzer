import streamlit as st
import pandas as pd
import csv
from jobspy import scrape_jobs

def create_custom_css() -> str:
    """Generate custom CSS for Streamlit styling."""
    return """
    <style>
    .main-title {
        color: #2C3E50;
        font-size: 2.5em;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
    }
    .job-card {
        background-color: black;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .job-card:hover {
        transform: scale(1.02);
    }
    </style>
    """

def scrape_job_listings(job_titles: list, location: str, results_wanted: int):
    """
    Scrape job listings with advanced configuration.
    
    Args:
        job_titles (list): List of job search terms
        location (str): Location for job search
        results_wanted (int): Number of results per job title
    
    Returns:
        DataFrame: Aggregated job listings
    """
    try:
        all_jobs = []
        
        for title in job_titles:
            jobs = scrape_jobs(
                site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
                search_term=title,
                location=location,
                results_wanted=results_wanted * 2, 
                hours_old=72,  
                country_indeed='India',
                job_type="fulltime",  
                is_remote=False,  
                linkedin_fetch_description=True,  
                verbose=1  
            )

            if not jobs.empty:
                jobs['location'].fillna('Location not specified', inplace=True)
                all_jobs.append(jobs.iloc[:results_wanted])
        
        combined_jobs = pd.concat(all_jobs, ignore_index=True)
        
        combined_jobs.drop_duplicates(subset=['job_url'], inplace=True)
        
        return combined_jobs
    
    except Exception as e:
        st.error(f"Error scraping jobs: {e}")
        return pd.DataFrame()


def render_job_card(job: pd.Series) -> str:
    """Generate HTML for a single job card."""
    return f"""
    <div class="job-card">
        <h3>{job.get('title', 'N/A')}</h3>
        <p><strong>Company:</strong> {job.get('company', 'N/A')}</p>
        <p><strong>Location:</strong> {job.get('location', 'N/A')}</p>
        <p><strong>Site:</strong> {job.get('site', 'N/A')}</p>
        <p><strong>Salary Range:</strong> 
            {job.get('min_amount', 'N/A')} - {job.get('max_amount', 'N/A')} 
            {job.get('interval', '')}
        </p>
        <a href="{job.get('job_url', '#')}" target="_blank">
            <button style="background-color: #2ECC71; color: white; border: none; padding: 10px 20px; border-radius: 5px;">
                View Job Details
            </button>
        </a>
    </div>
    """

def render_job_scraper():
    """Main Streamlit application for job scraping."""

    st.markdown(create_custom_css(), unsafe_allow_html=True)

    st.title("🔍 BMU Job Scraper")
    
    st.sidebar.header("🛠️ Search Configuration")
    
    job_titles = st.sidebar.text_area(
        "Enter job title:",
        placeholder="e.g., Software Engineer\nData Scientist\nProduct Manager",
        height=150
    )
    
    location = st.sidebar.text_input(
        "Location", 
        placeholder="e.g., San Francisco, CA"
    )
    
    results_wanted = st.sidebar.slider(
        "Results per Job Title", 
        min_value=1, 
        max_value=10, 
        value=4
    )

    if st.sidebar.button("🚀 Scrape Jobs"):
        if not job_titles.strip():
            st.error("Please enter at least one job title.")
            return
        
        if not location.strip():
            st.error("Please enter a location.")
            return
        
        job_titles_list = [title.strip() for title in job_titles.split("\n") if title.strip()]
        
        with st.spinner("Scraping job listings..."):
            jobs = scrape_job_listings(job_titles_list, location, results_wanted)
        
        if not jobs.empty:
            st.success(f"Found {len(jobs)} job listings!")
            
            for idx, job in jobs.iterrows():
                st.markdown(render_job_card(job), unsafe_allow_html=True)
            
            st.header("💾 Export Option")
            
            csv_data = jobs.to_csv(index=False, quoting=csv.QUOTE_NONNUMERIC)
            st.download_button(
                label="📥 Download Jobs as CSV",
                data=csv_data,
                file_name="job_listings.csv",
                mime="text/csv"
            )
        else:
            st.warning("No jobs found. Try adjusting your search parameters.")
