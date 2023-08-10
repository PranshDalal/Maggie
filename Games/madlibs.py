import speech_recognition as sr
import pyttsx3
import re

def listen_for_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio)
            print(f"You said: {user_input}")
            return user_input.lower()
        except sr.UnknownValueError:
            print("Sorry, could not understand your speech.")
            return ""

def madlibs_game():
    madlibs_template = "Once upon a time, there was a {noun} who had a {adjective} {noun_plural}. They loved to {verb} all day long."
    words_to_replace = re.findall(r'{(.*?)}', template)

    for word in words_to_replace:
        print(f"Please provide a {word}:")
        user_input = listen_for_input()
        template = template.replace(f"{{{word}}}", user_input, 1)

    print("\nYour Madlibs Story:")
    print(template)

    engine = pyttsx3.init()
    engine.say(template)
    engine.runAndWait()

if __name__ == "__main__":
    madlibs_game()
