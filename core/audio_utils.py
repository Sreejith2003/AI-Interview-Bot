import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
import time

# 🎙️ Record candidate’s voice and convert to text
def record_audio():
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


# 🔊 Convert text to audio and save
def text_to_speech(text):
    if not text or not text.strip():
        text = "I'm sorry, I didn't catch that. Could you please repeat?"
    tts = gTTS(text)
    filename = f"audio_{int(time.time())}.mp3"
    audio_path = os.path.join("audio_temp", filename)
    tts.save(audio_path)
    return audio_path
