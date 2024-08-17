import pyttsx3
import requests
import speech_recognition as sr
import os
import datetime
import wikipedia
import webbrowser
import pyjokes

# Initialize speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Set up constants
USERNAME = "Vansh"
BOTNAME = "JARVIS"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")

def take_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        if not 'exit' in query or 'stop' in query:
            speak("Okay, what's next?")
        else:
            hour = datetime.datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir, take care!")
            else:
                speak('Have a good day sir!')
            exit()
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query

def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def play_on_youtube(video):
    webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={video}")

def search_on_google(query):
    webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")

def tell_joke():
    speak(pyjokes.get_joke())

greet_user()
while True:
    query = take_user_input()
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        result = search_on_wikipedia(query)
        speak(result)
    elif 'youtube' in query:
        speak("Searching YouTube...")
        query = query.replace("youtube", "")
        result = play_on_youtube(query)
    elif 'google' in query:
        speak("Searching Google...")
        query = query.replace("google", "")
        result = search_on_google(query)
    elif 'joke' in query:
        tell_joke()
    elif 'exit' in query or 'stop' in query:
        hour = datetime.datetime.now().hour
        if hour >= 21 and hour < 6:
            speak("Good night sir, take care!")
        else:
            speak('Have a good day sir!')
        break
    else:
        speak("Sorry, I didn't understand that. Could you please try again?")