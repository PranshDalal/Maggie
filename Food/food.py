import requests
import speech_recognition as sr
import pyttsx3

YELP_API_KEY = 'API_KEY'

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

def get_random_restaurant(location, radius=2000, limit=50):
    endpoint = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': f'Bearer {YELP_API_KEY}'}
    params = {'term': 'restaurants', 'location': location,
              'radius': radius, 'limit': limit}

    response = requests.get(endpoint, headers=headers, params=params)
    data = response.json()

    if 'businesses' in data:
        return random_restaurant(data['businesses'])
    else:
        return None

def random_restaurant(businesses):
    import random
    random_index = random.randint(0, len(businesses) - 1)
    return businesses[random_index]

def find_random_restaurant_and_speak():
    speak("Hello! I'm here to help you find a random restaurant. Please tell me your location.")
    while True:
        user_input = recognize_speech()
        if 'exit' in user_input:
            speak("Goodbye!")
            break
        
        location = user_input
        restaurant = get_random_restaurant(location)

        if restaurant:
            name = restaurant['name']
            address = restaurant['location']['address1']
            phone = restaurant['phone']
            rating = restaurant['rating']

            response = f"The random restaurant near {location} is {name}. It is located at {address}. " \
                       f"You can contact them at {phone}. It has a rating of {rating} out of 5. Enjoy your meal!"
            speak(response)
            break
        else:
            response = f"Sorry, no restaurants found near {location}. Please try again."

        speak(response)
