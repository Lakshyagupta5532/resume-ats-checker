# 🎯 AI-Powered Resume ATS Checker

An intelligent resume screening tool that analyzes how well a resume matches a job — using AI to dynamically extract relevant skills instead of relying on a fixed keyword list.

## 🧩 The Problem

Most students and job seekers don't know **why** their resume gets rejected before a human even sees it. Many companies use ATS (Applicant Tracking Systems) to automatically filter resumes based on keyword matches with the job description — but candidates have no easy way to check this themselves before applying.

I built this tool to solve that exact problem for myself: **"Does my resume actually match what this job is asking for, and what am I missing?"**

## 💡 Why I Built It This Way

My first version used a fixed list of predefined skills to check resumes against — but this had a major limitation: it only worked for *known* skills I had manually added, and failed for any new or unique job role.

Real-world job requirements vary wildly across roles, so a static list wasn't practical. Instead, I integrated an **LLM (Gemini API)** to dynamically generate relevant skills for *any* job title or job description — making the tool generalize to roles I never explicitly coded for.

## ⚙️ How It Works

1. **Resume Upload** — User uploads their resume as a PDF
2. **Text Extraction** — `pdfplumber` extracts raw text from the PDF
3. **Skill Requirement Generation** — Depending on the mode:
   - If a job description is pasted, the app extracts key skills directly from it using YAKE (keyword extraction)
   - If only a job title is given, the Gemini API generates a list of commonly required skills for that role
4. **Matching** — The extracted resume text is compared against the required skills list (with smart matching for combined skills like "TensorFlow/PyTorch")
5. **Results** — The app displays a match percentage, skills found, and skills missing — so the user knows exactly what to improve

## ✨ Features

- 📤 PDF resume upload and text extraction
- 📋 Two input modes: paste a job description OR just enter a job title
- 🤖 AI-powered dynamic skill extraction (Gemini API)
- 📊 Match score with visual progress bar
- ✅ / ❌ Clear breakdown of matched vs missing skills
- 🔒 Secure API key handling using Streamlit Secrets

## 🛠️ Tech Stack

- **Python**
- **Streamlit** — web interface
- **pdfplumber** — PDF text extraction
- **YAKE** — keyword extraction from job descriptions
- **Google Gemini API** — dynamic skill generation for job titles
- **Streamlit Cloud** — deployment

## 🚀 Live Demo

🔗 [Try it here](https://resume-ats-checker-lakshya-gupta.streamlit.app/)

## 🖥️ Run Locally

```bash
git clone https://github.com/Lakshyagupta5532/resume-ats-checker.git
cd resume-ats-checker
pip install -r requirements.txt
```

Create a `.streamlit/secrets.toml` file and add your Gemini API key:
```toml
GEMINI_API_KEY = "your_api_key_here"
```

Then run:
```bash
streamlit run app.py
```

## 🧠 What I Learned

- Extracting and cleaning text from real-world PDF documents
- Working with NLP keyword extraction (YAKE) vs. LLM-based extraction — and when each is appropriate
- Integrating a third-party AI API into a working application
- Managing API keys and secrets securely in deployed apps
- Debugging real deployment issues (large file errors, dependency conflicts, accidental secret leaks on GitHub)

## 🔮 Future Improvements

- Add resume formatting/structure suggestions (not just keyword matching)
- Support multiple resume formats (DOCX, plain text)
- Allow comparison against multiple job descriptions at once
- Improve skill-matching using semantic similarity instead of exact text match
