from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from core.gemini_utils import generate_questions, evaluate_answer, generate_overall_feedback
from core.audio_utils import text_to_speech
import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
import PyPDF2

app = Flask(__name__)
app.secret_key = "interview_secret_key"

# Store interview state in session memory
session_data = {"questions": [], "current_index": 0, "responses": []}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    resume = request.files.get("resume")
    if not resume:
        return jsonify({"error": "No resume uploaded"}), 400

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        resume.save(temp_file.name)
        reader = PyPDF2.PdfReader(temp_file.name)
        resume_text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

    session_data["questions"] = generate_questions(resume_text)
    session_data["current_index"] = 0
    session_data["responses"] = []

    first_question = session_data["questions"][0]
    audio_path = text_to_speech(first_question)

    return jsonify({
        "first_question": first_question,
        "audio_path": f"/get_audio/{os.path.basename(audio_path)}"
    })


@app.route("/process_voice", methods=["POST"])
def process_voice():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file received"}), 400

    audio_file = request.files["audio"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
        audio_file.save(temp_audio.name)
        webm_path = temp_audio.name

    wav_path = webm_path.replace(".webm", ".wav")
    sound = AudioSegment.from_file(webm_path, format="webm")
    sound.export(wav_path, format="wav")
    os.remove(webm_path)

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            user_text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            user_text = ""
    os.remove(wav_path)

    index = session_data["current_index"]
    question = session_data["questions"][index]

    if not user_text.strip():
        feedback = "I couldn’t quite hear that clearly. Could you please repeat?"
        next_question = question
        final_feedback = None
    else:
        feedback = evaluate_answer(question, user_text)
        session_data["responses"].append({
            "question": question,
            "answer": user_text,
            "feedback": feedback
        })

        if index + 1 < len(session_data["questions"]):
            session_data["current_index"] += 1
            next_question = session_data["questions"][index + 1]
            final_feedback = None
        else:
            final_feedback = generate_overall_feedback(session_data["responses"])
            session["final_feedback"] = final_feedback
            return redirect(url_for("result"))

    audio_path = text_to_speech(next_question)

    return jsonify({
        "question_text": next_question,
        "user_text": user_text,
        "feedback": feedback,
        "audio_path": f"/get_audio/{os.path.basename(audio_path)}"
    })


@app.route("/finish_interview", methods=["GET"])
def finish_interview():
    if not session_data["responses"]:
        session["final_feedback"] = "Interview ended early. Not enough responses. Score: 0%"
    else:
        final_feedback = generate_overall_feedback(session_data["responses"])
        session["final_feedback"] = final_feedback
    return redirect(url_for("result"))


@app.route("/result")
def result():
    final_feedback = session.get("final_feedback", "No feedback available.")
    import re

    match = re.search(r"(\d+)%", final_feedback)
    score = int(match.group(1)) if match else 0
    summary = re.sub(r"Score:.*", "", final_feedback).strip()

    return render_template("result.html", feedback=summary, score=score)


@app.route("/get_audio/<filename>")
def get_audio(filename):
    return send_from_directory("audio_temp", filename)


if __name__ == "__main__":
    if not os.path.exists("audio_temp"):
        os.makedirs("audio_temp")
    app.run(debug=False)
