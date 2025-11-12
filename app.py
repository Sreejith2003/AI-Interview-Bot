from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai

# Initialize Flask
app = Flask(__name__)

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Ensure folders exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("static", exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_audio", methods=["POST"])
def process_audio():
    # Save uploaded audio file
    file = request.files["audio"]
    filepath = os.path.join("uploads", "user_audio.wav")
    file.save(filepath)

    # Convert speech → text
    recognizer = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand audio"}), 400
        except sr.RequestError as e:
            return jsonify({"error": str(e)}), 500

    # Generate AI response
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"The user said: '{text}'. Respond naturally to them.")
    ai_reply = response.text.strip() if response and response.text else "I couldn't generate a reply."

    # Convert AI reply → speech
    tts = gTTS(ai_reply)
    reply_audio_path = os.path.join("static", "response.mp3")
    tts.save(reply_audio_path)

    # Return text + audio path
    return jsonify({
        "recognized_text": text,
        "ai_reply": ai_reply,
        "audio_url": "/static/response.mp3"
    })

# Serve static audio (for playback)
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
