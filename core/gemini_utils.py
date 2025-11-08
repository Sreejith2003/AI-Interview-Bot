import google.generativeai as genai
import os
import re

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# -------------------------------
# 🧠 Generate Questions
# -------------------------------
def generate_questions(resume_text):
    intro_question = "Hi there! Welcome to your AI interview session. To begin, could you tell me a little about yourself?"

    prompt = f"""
    You are a friendly interviewer. Based on this resume, generate 3 job-relevant questions.
    Ask about technical skills, teamwork, achievements, and problem-solving.
    Keep the tone conversational and professional.

    Resume:
    {resume_text}
    """
    outro_question = "Thank you for attending the interview i will update your mark and share the feedback."

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    clean_output = re.sub(r"[*•#_`>-]+", "", response.text)
    followup_questions = [q.strip() for q in clean_output.split("\n") if q.strip()]
    return [intro_question] + followup_questions[:3] + [outro_question]


# -------------------------------
# 💬 Evaluate Each Answer
# -------------------------------
def evaluate_answer(question, answer):
    prompt = f"""
    You are a calm, professional interviewer evaluating a candidate's response.

    Question: {question}
    Answer: {answer}

    Give short, constructive feedback (2 lines max).
    Focus on clarity, confidence, and relevance.
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt).text.strip()
    feedback = re.sub(r"[*•#_`>-]+", "", response)
    return feedback


# -------------------------------
# 🏁 Overall Evaluation
# -------------------------------
def generate_overall_feedback(responses):
    combined = "\n".join(
        [f"Q: {r['question']}\nA: {r['answer']}\nFeedback: {r['feedback']}" for r in responses]
    )

    prompt = f"""
    You are an expert interviewer summarizing the candidate’s performance.

    Here is the full interview:
    {combined}

    Based on clarity, depth, confidence, and technical accuracy:
    - Write 3–4 sentences summarizing overall performance.
    - Then assign a score between 0 and 100 as 'Score: <number>%'.
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt).text.strip()
    return re.sub(r"[*•#_`>-]+", "", response)
