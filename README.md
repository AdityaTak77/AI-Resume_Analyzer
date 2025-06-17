# Resume Screening Tool

## Project Overview

The Resume Screening Tool is an innovative AI-powered platform designed to revolutionize the recruitment process by bridging the gap between students and recruiters through intelligent resume analysis and job matching.

##Demo
go to photos/demo1 and to photos/Screen Recording 2024-12-04 at 7.17.41 PM 

## Key Features

### For Students
- 🔍 Detailed Resume Analysis
- 💡 Personalized Improvement Suggestions
- 🤖 Interactive AI Chatbot Support
- 🎯 Job Recommendation System
- 🔗 LinkedIn Job Scraper

### For Recruiters
- 📊 Advanced Resume Ranking
- 🧠 Semantic Matching Algorithms
- 📈 Comprehensive Candidate Insights
- 📝 Exportable Candidate Reports

## Technology Stack
- Python
- Streamlit
- Hugging Face Embeddings
- Gemini Pro RAG
- Mixtral Groq Chat
- Natural Language Processing (NLP)
- Machine Learning Algorithms

## Prerequisites
- Python 3.8+
- API Keys:
  - Google AI Studio API Key (for Gemini)
  - Groq API Key

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/resume-screening-tool.git
cd resume-screening-tool
```

#### 2. In the Frontend Folder
Update `.env` in the frontend directory:
```
GOOGLE_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

#### In the Backend Folder
Update `.env` in the backend directory:
```
GOOGLE_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Install Dependencies
```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install required dependencies
pip install -r requirements.txt
```

### 4. Obtain API Keys
- **Google AI Studio API Key**: 
  1. Visit [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
  2. Create a new API key
  3. Copy the key and paste it in both `.env` files

- **Groq API Key**:
  1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
  2. Create a new API key
  3. Copy the key and paste it in both `.env` files

### 5. Run the Application
```bash
python -m streamlit run app.py
```

## Key Capabilities

### Resume Parsing and Analysis
- Extracts key information from resumes
- Evaluates ATS (Applicant Tracking System) compatibility
- Provides detailed compatibility breakdown

### Intelligent Matching
- Semantic matching between resumes and job descriptions
- Keyword analysis
- Format compatibility check
- Requirements coverage assessment

### Career Support
- Interactive chatbot for resume guidance
- Personalized job recommendations
- Visualization of career path opportunities
