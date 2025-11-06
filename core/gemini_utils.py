import google.generativeai as genai
import os
import random
import re

# -------------------------------
# ✅ Configure Gemini API Key
# -------------------------------
# Option 1: Hardcoded key (quick test)
#genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")

# Option 2: Environment variable (recommended)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# -------------------------------
# 🧠 Generate Diverse Questions
# -------------------------------
def generate_questions(resume_text):
    """
    Generate natural, friendly, and varied interview questions based on the resume.
    Avoid robotic tone — sound like a human interviewer.
    """
    prompt = f"""
    You are a friendly and curious interviewer having a natural conversation with a candidate.
    You just reviewed their resume.

    Resume:
    {resume_text}

    Generate 5 conversational interview questions that:
    - Sound human and engaging (not formal or robotic)
    - Each question focuses on a different area of the resume:
      technical skills, education, projects, achievements, teamwork, problem-solving, or goals
    - Use natural phrasing like:
      "That's interesting, could you tell me more about that?"
      "I see you worked on this — how was that experience?"
      "Good work! How did you handle challenges in that project?"

    Avoid any asterisks, markdown formatting, or lists with bullets.
    Write plain text only.
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    raw_output = response.text

    # Clean formatting symbols like '*', '-', etc.
    clean_output = re.sub(r"[*•#_`>-]+", "", raw_output)
    questions = [q.strip() for q in clean_output.split("\n") if q.strip()]
    random.shuffle(questions)
    return questions[:5]


# -------------------------------
# 💬 Conversational Feedback
# -------------------------------
def evaluate_answer(question, answer):
    """
    Respond casually to the candidate's answer.
    Sound warm, natural, and curious — like a real human interviewer.
    Avoid markdown, lists, or unnatural phrases.
    """
    prompt = f"""
    You are a friendly human interviewer responding naturally to a candidate's answer.
    You just asked:
    "{question}"

    The candidate said:
    "{answer}"

    Respond like a person in a conversation:
    - Start with a short compliment or natural acknowledgment (e.g. "Nice!", "Good one!", "That sounds great!")
    - Add a short follow-up question or curiosity ("What made you choose that approach?", "Could you tell me more about that?", "Interesting! How did you deal with challenges?")
    - Keep it under 1 sentences.
    - Avoid markdown, asterisks, bullets, or formatting.

    Output should be plain text only.
    
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt).text.strip()

    # Remove any unwanted markdown or symbols
    clean_response = re.sub(r"[*•#_`>-]+", "", response)
    return clean_response.strip()
