import os
import datetime
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as google_requests
from googleapiclient.discovery import build
import pyttsx3
import speech_recognition as sr

API_KEY = "AIzaSyCg7BpEYJB1yDIeiGsTS-D7R-aHJx9ygxQ"
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

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

def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = google.oauth2.credentials.Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google_requests())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def create_event(service, title, description, start_time, end_time):
    event = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
    }

    try:
        event = service.events().insert(calendarId="primary", body=event).execute()
        return event.get("id")
    except Exception as e:
        print(f"An error occurred while adding the event: {e}")
        return None

def add_event(service):
    title = input("Enter event title: ")
    description = input("Enter event description: ")
    date_str = input("Enter event date (YYYY-MM-DD): ")
    start_time_str = input("Enter start time (HH:MM): ")
    end_time_str = input("Enter end time (HH:MM): ")

    try:
        # Parse date and time strings
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.datetime.strptime(end_time_str, "%H:%M").time()

        # Combine date and time
        start_datetime = datetime.datetime.combine(date, start_time)
        end_datetime = datetime.datetime.combine(date, end_time)

        event_id = create_event(service, title, description, start_datetime.isoformat(), end_datetime.isoformat())

        if event_id:
            print("Event added successfully!")
            speak("Event added successfully!")
        else:
            print("Failed to add event.")
            speak("Failed to add event.")
    except ValueError:
        print("Invalid date or time format. Please use 'YYYY-MM-DD' for date and 'HH:MM' for time.")
        speak("Invalid date or time format. Please use 'YYYY-MM-DD' for date and 'HH:MM' for time.")

def get_events(service, date):
    start_time = datetime.datetime.combine(date, datetime.time())
    end_time = start_time + datetime.timedelta(days=1)

    try:
        request = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_time.isoformat() + "Z",
                timeMax=end_time.isoformat() + "Z", 
                singleEvents=True,
                orderBy="startTime",
            )
        )

        events_result = request.execute()
        events = events_result.get("items", [])
        return events
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds, developerKey=API_KEY)



    while True:
        print("Please pick from these options to interact with your calendar")
        speak("Please pick from these options to iteract with your calendar")
        print("1. Add event")
        speak("1. Add event")
        print("2. Get events for a specific date")
        speak("2. Get events for a specific date")
        print("3. Exit")
        speak("3. Exit")

        try:
            choice = recognize_speech()
            print(choice)
        except ValueError:
            print("Invalid choice. Try again.")
            continue

        if choice == "one":
            add_event(service)

        elif choice == "two":
            date = datetime.date.today()
            events = get_events(service, date)
            print(f"Events on {date}:")
            speak(f"Events on {date}:")
            for event in events:
                summary = event.get("summary", "No summary available")
                description = event.get("description", "No description available")
                print(f"- {summary}: {description}")
                speak(f"- {summary}: {description}")

        elif choice == "three":
            print("You are now exiting the calendar")
            speak("You are now exiting the calendar")
            break

        else:
            print("Invalid choice. Try again.")
            speak("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
