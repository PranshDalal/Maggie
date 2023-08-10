import random
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

def guess_the_number():
    secret_number = random.randint(1, 100)
    attempts = 0

    speak("Welcome to the Guess the Number game! Try to guess a number between 1 and 100.")
    
    while True:
        attempts += 1
        speak("Take a guess.")
        guess = recognize_speech()
        
        if "exit" in guess or "stop" in guess or "quit" in guess:
            speak("Thanks for playing. See you next time!")
            return

        try:
            guess_number = int(guess)
        except ValueError:
            speak("Please say a valid number.")
            continue
        
        if guess_number == secret_number:
            speak(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts.")
            break
        elif guess_number < secret_number:
            speak("The number is higher. Try again.")
        else:
            speak("The number is lower. Try again.")

if __name__ == "__main__":
    guess_the_number()
