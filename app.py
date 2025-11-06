from flask import Flask, request, jsonify, render_template, send_file
from core.resume_parser import extract_resume_text
from core.gemini_utils import generate_questions, evaluate_answer
from core.audio_utils import text_to_speech
import os
import tempfile
import speech_recognition as sr

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audio_temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

session_data = {
    "resume_text": "",
    "questions": [],
    "current_index": 0,
    "responses": []
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    file = request.files.get('resume')
    if not file:
        return jsonify({"error": "No resume uploaded"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    resume_text = extract_resume_text(filepath)
    questions = generate_questions(resume_text)

    session_data.update({
        "resume_text": resume_text,
        "questions": questions,
        "current_index": 0,
        "responses": []
    })

    first_question = questions[0]
    audio_path = text_to_speech(first_question)
    return jsonify({
        "message": "Resume processed successfully!",
        "first_question": first_question,
        "audio_path": f"/get_audio/{os.path.basename(audio_path)}"
    })


@app.route('/process_voice', methods=['POST'])
def process_voice():
    """Handles user's recorded voice, converts, transcribes, evaluates, and replies."""
    import tempfile
    import os
    import speech_recognition as sr
    from pydub import AudioSegment

    if 'audio' not in request.files:
        return jsonify({"error": "No audio file received"}), 400

    audio_file = request.files['audio']

    # Save the raw upload
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
        audio_file.save(temp_audio.name)
        webm_path = temp_audio.name

    # Convert to WAV
    wav_path = webm_path.replace(".webm", ".wav")
    try:
        sound = AudioSegment.from_file(webm_path, format="webm")
        sound.export(wav_path, format="wav")
        print(f"✅ Converted WebM to WAV: {wav_path}")
    except Exception as e:
        os.remove(webm_path)
        return jsonify({"error": f"Audio conversion failed: {str(e)}"}), 400
    finally:
        if os.path.exists(webm_path):
            os.remove(webm_path)

    # Transcribe using SpeechRecognition
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            user_text = recognizer.recognize_google(audio_data)
            print(f"🗣️ User said: {user_text}")
    except sr.UnknownValueError:
        user_text = ""
        print("⚠️ Could not understand audio.")
    except Exception as e:
        print("❌ Speech recognition error:", e)
        user_text = ""
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

    # Handle case: empty or failed speech
    index = session_data["current_index"]
    question = session_data["questions"][index]

    if not user_text.strip():
        feedback = "I couldn’t quite catch that. Could you please repeat?"
        next_question = question
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
        else:
            next_question = "That’s the end of our interview — great job!"

    response_text = f"{feedback} {next_question}"
    audio_path = text_to_speech(response_text)

    return jsonify({
        "question_text": next_question,
        "user_text": user_text,
        "feedback": feedback,
        "audio_path": f"/get_audio/{os.path.basename(audio_path)}"
    })



@app.route('/get_audio/<filename>')
def get_audio(filename):
    return send_file(os.path.join(AUDIO_FOLDER, filename))


if __name__ == '__main__':
    app.run(debug=True)
