import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3  # Local text-to-speech library
import time
import threading
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Set up Gemini API
KEY = 'AIzaSyCKA_SwVEjM3TzvvXAzD9pEsjwRBJVf1_Y'
genai.configure(api_key=KEY)

# Configure generation settings for the Gemini API
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,  # Reduced token limit to speed up responses
    "response_mime_type": "text/plain",
}

# Create the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Start a new chat session
chat_session = model.start_chat(history=[])

# Initialize pyttsx3 for faster, local text-to-speech
engine = pyttsx3.init()

# Function for faster text-to-speech using pyttsx3
def talk(audio):
    print(Fore.GREEN + audio)  # Color the output green
    engine.say(audio)
    engine.runAndWait()

# Function for speech-to-text
def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(Fore.YELLOW + "Listening for your command...")  # Change text color to yellow
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        print(Fore.YELLOW + "Analyzing...")  # Change text color to yellow

    try:
        command = r.recognize_google(audio).lower()
        print(Fore.CYAN + f"You said: {command}")  # Color the recognized command cyan
        time.sleep(2)
    except sr.UnknownValueError:
        print(Fore.RED + "Sorry, I couldn't hear you clearly. Could you please repeat?")  # Color error message red
        command = myCommand()
    
    return command

# Function to process speech input and generate a response from Gemini
def process_speech(command):
    # Send the user's speech input to the Gemini API for response generation
    response = chat_session.send_message(command)
    
    # Extract the response from Gemini
    response_text = response.text
    print(Fore.MAGENTA + f"TARS says: {response_text}")  # Color Gemini's response magenta

    # Convert Gemini's text response to speech
    talk(response_text)

# Main loop: continuously listen for commands and process them
def listen_and_respond():
    while True:
        command = myCommand()  # Convert speech to text
        process_speech(command)  # Get a response from Gemini and convert it to speech

# Run the listening loop in a separate thread to avoid blocking
listener_thread = threading.Thread(target=listen_and_respond)
listener_thread.start()
