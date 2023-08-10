import requests
import pyttsx3


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def fetch_random_joke():
    base_url = "https://v2.jokeapi.dev/joke/Any"
    
    response = requests.get(base_url)
    data = response.json()
    
    if response.status_code == 200 and data["type"] == "single":
        return data["joke"]
    elif response.status_code == 200 and data["type"] == "twopart":
        return f"{data['setup']} {data['delivery']}"
    else:
        return "Failed to fetch a joke"

if __name__ == "__main__":
    joke = fetch_random_joke()
    print("Here's a random joke for you:")
    speak(joke)
