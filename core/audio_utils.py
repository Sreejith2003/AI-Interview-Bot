import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
import time
import uuid
from pydub import AudioSegment


# 🎙️ (Optional) Local audio recording for CLI testing (not used in Flask)
def record_audio():
    """
    Record audio from the system microphone (for testing locally).
    Not used inside Flask app (browser records instead).
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... please answer the question.")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("🗣️ You said:", text)
        return text
    except sr.UnknownValueError:
        print("⚠️ Could not understand audio.")
        return None
    except sr.RequestError as e:
        print("❌ Speech Recognition Error:", e)
        return None


# 🔊 Convert question text → speech and save to static folder
def text_to_speech(text):
    """
    Converts given text to speech using Google TTS and saves the file
    inside the static/ folder so Flask can serve it.
    """
    if not text or not text.strip():
        text = "I'm sorry, I didn't catch that. Could you please repeat?"

    # Create unique filename
    filename = f"{uuid.uuid4()}.mp3"
    static_dir = "audio_temp"
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    file_path = os.path.join(static_dir, filename)

    # Generate and save TTS
    try:
        tts = gTTS(text=text, lang="en")
        tts.save(file_path)
        print(f"✅ TTS saved at: {file_path}")
    except Exception as e:
        print(f"❌ Error during TTS: {e}")
        return None

    return file_path


# 🧠 Convert user voice (WebM → WAV → Text)
def convert_audio_to_text(webm_path):
    """
    Converts uploaded .webm file to text using Google Speech Recognition.
    Flask backend uses this after receiving user's recorded answer.
    """
    try:
        # Convert WebM to WAV
        wav_path = webm_path.replace(".webm", ".wav")
        sound = AudioSegment.from_file(webm_path, format="webm")
        sound.export(wav_path, format="wav")
        os.remove(webm_path)

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                text = ""
        os.remove(wav_path)
        return text

    except Exception as e:
        print(f"❌ Audio conversion failed: {e}")
        return ""
