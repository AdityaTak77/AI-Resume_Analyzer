import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.base import Runnable
# from crewai import LLM
import matplotlib.pyplot as plt
import requests
import re
# Set up Groq API key
load_dotenv()  # Load environment variables from .env file
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY") 

# llm = LLM(
#     model="gemini/gemini-1.5-pro-002",
#     api_key="AIzaSyB7C_pdLgIGf9RHH5f9w9_nc90BI7sLAbE"
# )

from langchain_google_genai import ChatGoogleGenerativeAI
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


# Initialize the ChatGroq model with the specified model name
llm1 = ChatGroq(model_name="deepseek-r1-distill-llama-70b")

def plot_ats_breakdown(keyword_match, format_compatibility, requirements_coverage):
    labels = ['Keyword Match', 'Format Compatibility', 'Requirements Coverage']
    values = [keyword_match, format_compatibility, requirements_coverage]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['blue', 'green', 'orange'])
    plt.xlabel("ATS Compatibility Metrics")
    plt.ylabel("Percentage")
    plt.title("ATS Compatibility Breakdown")
    plt.ylim(0, 100)

    # Save the figure to a file
    plt.savefig("ats_compatibility_breakdown.png")

    # Display the plot
    plt.show()

def extract_scores(response_text):
    """
    Extract numerical scores from the AI response.
    """
    keyword_match = re.search(r"Keyword Match Rate:\s*(\d+)%", response_text)
    format_compatibility = re.search(r"Format Compatibility:\s*(\d+)%", response_text)
    requirements_coverage = re.search(r"Key Requirements Coverage:\s*(\d+)%", response_text)

    # Extract values or default to 0 if not found
    keyword_match = int(keyword_match.group(1)) if keyword_match else 0
    format_compatibility = int(format_compatibility.group(1)) if format_compatibility else 0
    requirements_coverage = int(requirements_coverage.group(1)) if requirements_coverage else 0

    return keyword_match, format_compatibility, requirements_coverage

def analyze_resume(full_resume, job_description):
    # Template for analyzing the resume against the job description
    template = """
You are an advanced AI assistant specialized in resume analysis, ATS optimization, and recruitment matching. Analyze the provided resume against the job description and provide a detailed evaluation.

*ATS COMPATIBILITY SCORE*:
- Keyword Match Rate: XX%
- Format Compatibility: XX%
- Key Requirements Coverage: XX%

*MATCH ANALYSIS*:
1. Overall Match Score: [0-100%]
- Technical Skills: XX%
- Experience Level: XX%
- Education: XX%
- Industry Alignment: XX%

2. Skills Breakdown:
- Strong Matches:
  - [List exact matching skills with context]
  - [Additional matching skills]
  - [Additional matching skills]

- Partial Matches:
  - [List related/transferable skills]
  - [Additional partial matches]
  - [Additional partial matches]

- Missing Critical Skills:
  - [List required skills not found]
  - [Additional missing skills]
  - [Additional missing skills]

- Additional Relevant Skills:
  - [List candidate's bonus qualifications]
  - [Additional bonus skills]
  - [Additional bonus skills]

3. Experience Alignment:
- Years of Experience: [Required vs. Actual]
- Industry Experience: [Relevance Analysis]
- Project Scope: [Scale and Complexity Match]
- Management Level: [Required vs. Demonstrated]

*DETAILED EVALUATION*:

1. Keyword Optimization:
- High-Impact Keywords Present:
  - [List with frequency]
  - [Additional keywords]
  - [Additional keywords]

- Missing Critical Keywords:
  - [List with importance level]
  - [Additional missing keywords]
  - [Additional missing keywords]

- Keyword Context Quality:
  - [Assessment of keyword usage]
  - [Additional context]
  - [Additional context]

2. Qualifications Assessment:
- Required Qualifications: [Met/Partially Met/Not Met]
- Preferred Qualifications: [Met/Partially Met/Not Met]
- Additional Relevant Qualifications:
  - [Qualification 1]
  - [Qualification 2]
  - [Qualification 3]

3. Technical Proficiency:
- Required Technical Skills: [Analysis]
- Technical Stack Alignment: [Evaluation]
- Tools & Platforms:
  - [Tool/Platform 1]
  - [Tool/Platform 2]
  - [Tool/Platform 3]

4. Soft Skills Analysis:
- Leadership & Management: [Assessment]
- Communication: [Evaluation]
- Problem-Solving: [Analysis]
- Team Collaboration: [Assessment]

*RECOMMENDATIONS*:

1. For the Candidate:
- Resume Optimization Suggestions:
  - [Suggestion 1]
  - [Suggestion 2]
  - [Suggestion 3]

- Skills Development Priorities:
  - [Priority 1]
  - [Priority 2]
  - [Priority 3]

- Experience Gaps to Address:
  - [Gap 1]
  - [Gap 2]
  - [Gap 3]

2. For the Interview:
- Interview Focus Areas:
  - [Focus Area 1]
  - [Focus Area 2]
  - [Focus Area 3]

- Risk Assessment:
  - [Risk 1]
  - [Risk 2]
  - [Risk 3]

- Training & Development Needs:
  - [Need 1]
  - [Need 2]
  - [Need 3]

3. Additional Screening Recommendations:
- Technical Assessments:
  - [Assessment Area 1]
  - [Assessment Area 2]
  - [Assessment Area 3]

- Background Verification:
  - [Verification Area 1]
  - [Verification Area 2]
  - [Verification Area 3]

- Reference Check Focus:
  - [Focus Area 1]
  - [Focus Area 2]
  - [Focus Area 3]

*COMPETITIVE ANALYSIS*:
- Market Position: [How candidate compares to market standards]
- Salary Range Alignment: [Based on experience and skills]
- Growth Potential: [Career trajectory assessment]

*FINAL VERDICT*:
- Overall Recommendation: [Strong Match/Moderate Match/Weak Match]
- Key Strengths:
  - [Strength 1]
  - [Strength 2]
  - [Strength 3]

- Critical Gaps:
  - [Gap 1]
  - [Gap 2]
  - [Gap 3]

- Time-to-Productivity Estimate: [Immediate/1-3 months/3+ months]

Resume: {resume}
Job Description: {job_description}

Analysis:
"""
    prompt = PromptTemplate(  # Create a prompt template with input variables
        input_variables=["resume", "job_description"],
        template=template
    )

    # Create a chain combining the prompt and the language model
    chain = prompt | llm
    try:
        # Invoke the chain with input data
        response = chain.invoke({"resume": full_resume, "job_description": job_description})

        if response and response.content:
            # Extract scores dynamically from the response
            keyword_match, format_compatibility, requirements_coverage = extract_scores(response.content)

            # Generate the ATS compatibility breakdown graph
            plot_ats_breakdown(keyword_match, format_compatibility, requirements_coverage)

            return response.content  # Return the content of the response
        else:
            raise ValueError("Response content is empty or invalid.")

    except Exception as e:
        # Handle potential errors gracefully
        print(f"An error occurred while analyzing the resume: {e}")
        return "Error: Unable to analyze resume. Please check inputs and try again."