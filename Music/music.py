import webbrowser
from youtube_search import YoutubeSearch
import pyttsx3
import speech_recognition as sr

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        text = recognizer.recognize_google(audio).lower()
        return text
    except sr.UnknownValueError:
        return "I didn't understand. Please try again."
    except sr.RequestError:
        return "Sorry, I couldn't access the Google Speech Recognition service."

def play_youtube_video():
    try:
        speak("Enter the music you want to play")
        search_query = recognize_speech()
        results = YoutubeSearch(search_query, max_results=1).to_dict()
        if results:
            video_url = "https://www.youtube.com" + results[0]['url_suffix']
            webbrowser.open(video_url)
            print(f"Opening: {results[0]['title']}")
        else:
            print("No results found for the query:", search_query)
    except Exception as e:
        print("Error:", str(e))
