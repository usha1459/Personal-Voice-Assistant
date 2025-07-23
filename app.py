import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import streamlit as st
import random

# ------------ Helper -------------
def info_box(text):
    st.markdown('<div class="wide-output">', unsafe_allow_html=True)
    st.info(text)
    st.markdown('</div>', unsafe_allow_html=True)

def speak(text):
    info_box(f"🗣️ Baby Siri says: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty('voice', engine.getProperty('voices')[0].id)
        engine.setProperty('volume', 1.0)
        engine.setProperty('rate', 180)
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        info_box("⚠️ Voice engine busy. Try again.")

def listen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.markdown("<div class='listening'>🎙️ Listening... Speak now.</div>", unsafe_allow_html=True)
            recognizer.pause_threshold = 0.8
            audio = recognizer.listen(source)
            st.markdown("""<style>.listening {display: none !important;}</style>""", unsafe_allow_html=True)
            try:
                command = recognizer.recognize_google(audio, language='en-in')
                st.success(f"✅ You said: {command}")
                return command.lower()
            except sr.UnknownValueError:
                info_box("⚠️ Sorry, I couldn't understand.")
            except sr.RequestError:
                info_box("🔌 Internet issue. Try again.")
    except Exception as mic_err:
        info_box(f"🎤 Microphone error: {mic_err}")
    return ""

def process_command(command):
    if 'what is the time' in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
    elif 'hi' in command:
        speak("Hi")
    elif 'hello' in command:
        speak("Hello")
    elif 'greetings' in command:
        speak("Greetings")
    elif 'thank you' in command or 'thanks' in command:
        speak(f"You are welcome")
    elif "today's date" in command:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")
    elif 'open google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'play music' in command:
        speak("Playing a music video from YouTube")
        music_links = [
            "https://www.youtube.com/watch?v=irKtQv3q9KI",
            "https://www.youtube.com/watch?v=Gg48H-lrZHo",
            "https://www.youtube.com/watch?v=YZy1ala9lt8",
            "https://www.youtube.com/watch?v=gJLVTKhTnog"
        ]
        webbrowser.open(random.choice(music_links))
    elif 'search for' in command:
        query = command.split('search for')[-1].strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
    elif 'your name' in command:
        speak("I am your Baby Siri Voice Assistant")
    elif 'how are you' in command:
        speak("I'm doing great! Thanks for asking.")
    elif 'who made you' in command or 'who created you' in command:
        speak("I was created by Prathyusha.")
    elif 'who is your creator' in command:
        speak("Prathyusha is my amazing creator!")
    elif 'how old are you' in command:
        speak("I was born recently in your code! Still learning every day.")
    elif 'what is your purpose' in command:
        speak("To help you with anything I can. I'm here to assist you!")
    elif 'sing a song' in command:
        speak("Twinkle, twinkle, little star... Just kidding, I can’t sing well yet!")
    elif 'motivate me' in command:
        speak("You are capable of amazing things. Keep going, champion!")
    elif 'tell me a joke' in command or 'tell me another joke' in command:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my computer I needed a break, and it said 'no problem — I’ll go to sleep.'",
            "Why was the math book sad? Because it had too many problems."
        ]
        speak(random.choice(jokes))
    elif 'what can you do' in command:
        speak("I can tell the time, date, open websites, answer questions, play music, and more. I’m always learning!")
    elif 'stop' in command or 'exit' in command:
        speak("Bye Bye")
    else:
        speak("Sorry, I can't do this yet")

# ------------ Page Setup -------------
st.set_page_config(page_title="🧠 Baby Siri", page_icon="🎹", layout="wide")

# ------------ CSS -------------
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #000000;
    background-image: linear-gradient(to right, #000000, #330000);
    font-family: 'Segoe UI', sans-serif;
    color: white;
}
footer {visibility: hidden;}

.glow-box {
    background-color: #1a1a1a;
    box-shadow: 0 0 35px red;
    border-radius: 25px;
    padding: 2rem;
    margin: 3rem auto 1rem auto;
    text-align: center;
    max-width: 900px;
}
.glow-box h1 {
    font-size: 3rem;
    color: #ff4d4d;
}
.glow-box h4 {
    font-size: 1.4rem;
    color: #ffcccc;
}

.wide-output .stAlert {
    max-width: 900px;
    margin: auto;
    background-color: #1f1f1f !important;
    color: #ffffff !important;
    border-left: 6px solid #ff4d4d !important;
    box-shadow: 0px 0px 10px #ff4d4d;
}

.listening {
    color: #ff4d4d;
    text-align: center;
    font-weight: bold;
    font-size: 1.5rem;
    margin-top: 2rem;
    animation: pulse 1s infinite;
}
@keyframes pulse {
    0% {opacity: 1;}
    50% {opacity: 0.5;}
    100% {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# ------------ Title -------------
st.markdown("""
<div class="glow-box">
    <h1>🎹 Baby Siri</h1>
    <h4>Your personal voice assistant</h4>
</div>
""", unsafe_allow_html=True)

# ------------ Session State -------------
if 'start_triggered' not in st.session_state:
    st.session_state['start_triggered'] = False
if 'greeted' not in st.session_state:
    st.session_state['greeted'] = False
if 'name' not in st.session_state:
    st.session_state['name'] = ""

# ------------ Name Prompt -------------
if not st.session_state['name']:
    user_name = st.text_input("👤 Please enter your name to begin:")
    if user_name:
        st.session_state['name'] = user_name
        st.rerun()

# ------------ Button + Logic -------------
if st.session_state['name']:
    start_button = st.button("🚀 Start Talking")

    if start_button or st.session_state['start_triggered']:
        st.session_state['start_triggered'] = True

    if not st.session_state['greeted']:
        speak(f"Hello, I am your Baby Siri. How can I help you, {st.session_state['name']}?")
        st.session_state['greeted'] = True

    user_command = listen()
    if user_command:
        if 'stop' in user_command or 'exit' in user_command:
            speak("Bye Bye")
            st.session_state['start_triggered'] = False
            st.session_state['greeted'] = False
        else:
            process_command(user_command)
            st.rerun()
