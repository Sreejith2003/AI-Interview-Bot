# AI-Interview-Bot

An AI-powered voice-based interview system built with Flask that conducts personalized interviews using your uploaded resume.
The bot asks intelligent questions, listens to your voice responses, evaluates them using Google Gemini, and finally provides feedback and an overall score.

# 🚀 Features

🎙️ Voice Interaction — Speak naturally; no typing required

📄 Resume-Aware Questions — Questions are generated based on your uploaded resume

💬 Smart Feedback — AI evaluates answers and gives constructive feedback

🧩 Realistic Conversation Flow — Human-like tone and adaptive questioning

🏁 Final Evaluation — Overall feedback and performance score at the end

🎧 Text-to-Speech and Speech-to-Text — Using gTTS and Google SpeechRecognition

🌗 Dark Modern UI — Built with a professional black & blue theme



# ⚙️ Installation

1️⃣ Clone this repository
```
git clone https://github.com/Sreejith2003/AI-Interview-Bot.git
```
```
cd ai-voice-interview-bot
```
2️⃣ Create a virtual environment
```
python -m venv Interview
```

3️⃣ Activate the environment

Windows (PowerShell):

```
Interview\Scripts\activate
```

Mac/Linux:
```
source Interview/bin/activate
```
4️⃣ Install dependencies
```
pip install -r requirements.txt
```

5️⃣ Install FFmpeg

PyDub and SpeechRecognition require FFmpeg.
Download and install it from https://ffmpeg.org/download.html
,
then add its path to your system environment variables.

# 🔑 Environment Setup

You need a Google Gemini API key.

Get your key from Google AI Studio
.

Set it as an environment variable:

Windows (PowerShell):

```
setx GOOGLE_API_KEY "your_gemini_api_key_here"
```

Mac/Linux:
```
export GOOGLE_API_KEY="your_gemini_api_key_here"
```
▶️ Run the Application
```
python app.py
```

Then open your browser and visit:
👉 http://127.0.0.1:5000/

🧠 How It Works

1️⃣ Upload your resume (PDF).
2️⃣ The Gemini model analyzes your resume and generates personalized interview questions.
3️⃣ The bot speaks the first question aloud using gTTS.
4️⃣ You answer verbally — your voice is recorded and transcribed via SpeechRecognition.
5️⃣ Gemini evaluates your answer and gives immediate feedback.
6️⃣ Once all questions are completed, the bot provides a final performance score and summary.

🏁 Result Page

At the end of your interview:

You’ll see an animated circular score (e.g., 83%)

A summary paragraph analyzing your overall performance

A “Start New Interview” button to retry anytime

📦 Dependencies
Flask
google-generativeai
SpeechRecognition
gTTS
PyDub
PyPDF2
ffmpeg

🌱 Future Enhancements

🧍‍♂️ Personalized interviewer voices (custom TTS voices)

📊 Detailed analytics dashboard for performance tracking

🎯 Question category classification (Technical / HR / Behavioral)

☁️ Integration with cloud storage for saving interview history

🔉 Optional real-time subtitles while answering