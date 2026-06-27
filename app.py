import streamlit as st
import pdfplumber
from google import genai

# ====== CONFIG ======
st.set_page_config(page_title="SmartATS - Resume Checker", page_icon="🎯", layout="wide")

API_KEY = st.secrets["GEMINI_API_KEY"]  # apni key yaha daal
client = genai.Client(api_key=API_KEY)

# ====== CUSTOM CSS ======
st.markdown("""
<style>
.hero {
    text-align: center;
    padding: 2rem 0 1rem 0;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}
.hero p {
    font-size: 1.1rem;
    color: #888;
}
.stButton button {
    border-radius: 8px;
    font-weight: 600;
    height: 3rem;
}
</style>
""", unsafe_allow_html=True)

# ====== FUNCTIONS ======
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def get_skills_from_title(job_title):
    prompt = f"""List the top 15 most important technical skills, tools, and qualifications 
    required for a {job_title} role. Return ONLY a list separated by the pipe symbol (|), 
    nothing else. No explanations, no numbering, no parentheses.
    Example format: python|sql|machine learning|aws"""
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return [s.strip().lower() for s in response.text.split("|")]

def get_skills_from_jd(job_description):
    prompt = f"""Extract the top 15 most important technical skills, tools, and qualifications 
    mentioned in this job description. Return ONLY a list separated by the pipe symbol (|), 
    nothing else. No explanations, no numbering, no parentheses.
    
    Job Description: {job_description}
    
    Example format: python|sql|machine learning|aws"""
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return [s.strip().lower() for s in response.text.split("|")]

def check_skills_in_resume(skills, resume_text):
    resume_lower = resume_text.lower()
    found, missing = [], []
    for skill in skills:
        parts = skill.replace('&', '/').split('/')
        if any(part.strip() in resume_lower for part in parts):
            found.append(skill)
        else:
            missing.append(skill)
    return found, missing

# ====== HERO / LANDING SECTION ======
st.markdown("""
<div class="hero">
    <h1>🎯 SmartATS</h1>
    <p>AI-powered resume analyzer — see how well you match any job, instantly.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ====== INPUT MODE TOGGLE ======
mode = st.radio(
    "How do you want to check your match?",
    ["📋 Paste a Job Description", "💼 Just Enter Job Title"],
    horizontal=True
)

st.write("")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 Upload Your Resume")
    uploaded_resume = st.file_uploader("Choose PDF file", type="pdf")

with col2:
    if mode == "📋 Paste a Job Description":
        st.subheader("📋 Job Description")
        job_description = st.text_area("Paste the job description here", height=180)
        job_title = None
    else:
        st.subheader("💼 Job Title")
        job_title = st.text_input("E.g. AIML Engineer, Data Analyst, Backend Developer")
        job_description = None

st.write("")
check_button = st.button("🔍 Analyze My Resume", type="primary", use_container_width=True)

# ====== RESULTS ======
if check_button:
    valid_input = (mode == "📋 Paste a Job Description" and job_description) or \
                  (mode == "💼 Just Enter Job Title" and job_title)

    if uploaded_resume is not None and valid_input:
        with st.spinner("Analyzing with AI..."):
            resume_text = extract_text_from_pdf(uploaded_resume)

            if mode == "📋 Paste a Job Description":
                required_skills = get_skills_from_jd(job_description)
            else:
                required_skills = get_skills_from_title(job_title)

            found_skills, missing_skills = check_skills_in_resume(required_skills, resume_text)
            match_percentage = (len(found_skills) / len(required_skills)) * 100 if required_skills else 0

        st.divider()
        st.subheader("📊 Your Results")

        score_col1, score_col2 = st.columns([1, 3])
        with score_col1:
            st.metric("Match Score", f"{match_percentage:.1f}%")
        with score_col2:
            st.progress(min(int(match_percentage), 100))

        skill_col1, skill_col2 = st.columns(2)
        with skill_col1:
            st.markdown("### ✅ Skills You Have")
            for skill in found_skills:
                st.success(skill.capitalize())
            if not found_skills:
                st.info("No matching skills found")

        with skill_col2:
            st.markdown("### ❌ Skills To Add")
            for skill in missing_skills:
                st.error(skill.capitalize())
            if not missing_skills:
                st.info("Great! No missing skills")
    else:
        st.warning("⚠️ Please upload a resume and provide job info")