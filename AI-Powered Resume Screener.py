# ============================================================
#   PROJECT 1 — AI-Powered Resume Screener
#   Tools used: Python, Anthropic Claude API, Pandas, JSON
# ============================================================

# These are called "imports" — we bring in tools we need
import anthropic    # to talk to Claude AI (free tier available)
import pandas as pd # to read/store resume data
import json         # to handle structured output from AI

# ── STEP 1: Set your Anthropic API key ──────────────────────
# Get your FREE key from: https://console.anthropic.com
# Click "Get API Keys" → Create Key → copy and paste it below
client = anthropic.Anthropic(api_key="your-anthropic-api-key-here")

# ── STEP 2: Define the Job Description ──────────────────────
job_description = """
We are looking for a fresher Python Developer with:
- Knowledge of Python and data libraries (Pandas, NumPy)
- Familiarity with databases like MongoDB or SQL
- Basic understanding of APIs or AI tools
- Good communication and willingness to learn
"""

# ── STEP 3: Define the Resume Text ──────────────────────────
resume_text = """
Name: Arjun Mehta
Skills: Python, Pandas, NumPy, Matplotlib, MongoDB, MySQL, Node.js
Projects:
  - Built a sales data analysis dashboard using Pandas and Matplotlib
  - Created an AI chatbot using OpenAI API with prompt engineering
  - Developed a student management system using Node.js and MongoDB
Education: B.Tech Computer Science, GTU, CGPA 8.1
Certifications: Python for Everybody (Coursera), MongoDB Basics
"""

# ── STEP 4: Build the Prompt ────────────────────────────────
def build_prompt(resume, job_desc):
    return f"""
You are an expert HR recruiter. Evaluate this resume against the job description.

JOB DESCRIPTION:
{job_desc}

CANDIDATE RESUME:
{resume}

Respond ONLY in this exact JSON format with no extra text:
{{
  "match_score": <number from 0 to 100>,
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "verdict": "Recommended" or "Not Recommended",
  "summary": "2-3 sentence overall summary of the candidate"
}}
"""

# ── STEP 5: Call the Claude API ─────────────────────────────
def screen_resume(resume, job_desc):
    prompt = build_prompt(resume, job_desc)

    # This sends our prompt to Claude and gets a response
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # fast and free-tier friendly model
        max_tokens=1024,
        system="You are an expert HR recruiter. Always reply in valid JSON only.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the text from Claude's response
    raw_text = response.content[0].text

    # Clean it up in case there are any backticks around the JSON
    clean_text = raw_text.strip().strip("```json").strip("```").strip()

    # Convert the text into a Python dictionary
    result = json.loads(clean_text)
    return result

# ── STEP 6: Display the Results Nicely ──────────────────────
def display_result(result):
    print("\n" + "="*50)
    print("       RESUME SCREENING RESULT")
    print("="*50)
    print(f"\n Match Score  : {result['match_score']} / 100")
    print(f" Verdict      : {result['verdict']}")
    print(f"\n Summary      : {result['summary']}")
    print("\n Strengths:")
    for s in result['strengths']:
        print(f"   + {s}")
    print("\n Weaknesses:")
    for w in result['weaknesses']:
        print(f"   - {w}")
    print("\n" + "="*50)

# ── STEP 7: Save Results to CSV using Pandas ────────────────
def save_to_csv(resume_name, result):
    data = {
        "Candidate"   : [resume_name],
        "Match Score" : [result['match_score']],
        "Verdict"     : [result['verdict']],
        "Summary"     : [result['summary']],
        "Strengths"   : [", ".join(result['strengths'])],
        "Weaknesses"  : [", ".join(result['weaknesses'])],
    }
    df = pd.DataFrame(data)
    df.to_csv("screening_results.csv", index=False)
    print("\n Results saved to screening_results.csv")

# ── STEP 8: Run Everything ───────────────────────────────────
if __name__ == "__main__":
    print("Screening resume... please wait...")
    result = screen_resume(resume_text, job_description)
    display_result(result)
    save_to_csv("Arjun Mehta", result)

# ============================================================
#   HOW TO RUN THIS FILE
#   1. Install the library:
#      pip install anthropic pandas
#
#   2. Get your FREE API key:
#      Go to https://console.anthropic.com → API Keys → Create
#      Paste it on line 13 replacing "your-anthropic-api-key-here"
#
#   3. Run in terminal:
#      python resume_screener.py
# ============================================================