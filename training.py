import sys
import speech_recognition as sr
import pyttsx3
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
import nltk
import requests

from my_calendar import main as calendar_main

from Food.food import find_random_restaurant_and_speak

from Games.guess_game import guess_the_number
from Games.madlibs import madlibs_game

from Jokes.jokes import fetch_random_joke

from Music.music import play_youtube_video

nltk.download('punkt')

stemmer = LancasterStemmer()
wake_word = "hey maggie"

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

with open("intents.json") as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = np.array(training)
output = np.array(output)

class ChatbotModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ChatbotModel, self).__init__()
        self.hidden_size = hidden_size
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return F.softmax(x, dim=1)

input_size = len(training[0])
hidden_size = 8
output_size = len(output[0])

model = ChatbotModel(input_size, hidden_size, output_size)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()


def talk(text):
    engine.say(text)
    engine.runAndWait()

def train_model(model, optimizer, criterion, epochs):
    for epoch in range(epochs):
        optimizer.zero_grad()
        inputs = torch.tensor(training, dtype=torch.float32)
        targets = torch.tensor(np.argmax(output, axis=1), dtype=torch.long)
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        if (epoch+1) % 100 == 0:
            print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item()}")

train_model(model, optimizer, criterion, epochs=1000)

torch.save(model.state_dict(), "model.pt")


def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            user_input = listener.recognize_google(voice)
            user_input = user_input.lower()
    except:
        pass
    return user_input

def generate_response(user_input):
    inp = user_input
    input_data = torch.tensor(bag_of_words(
        inp, words), dtype=torch.float32).unsqueeze(0)
    output = model(input_data)
    _, predicted = torch.max(output, dim=1)
    tag = labels[predicted.item()]

    if tag == "games":
        guess_game()
    elif tag == "food":
        find_random_restaurant_and_speak()
    elif tag == "calendar":
        calendar_main()
    elif tag == "music":
        play_youtube_video()
    elif tag == "joke":
        joke = fetch_random_joke()
        talk(joke)
    else:
        for intent in data["intents"]:
            if intent['tag'] == tag:
                responses = intent['responses']
                break
        else:
            responses = []

        response = random.choice(responses)
        return response
    
def guess_game():
    guess_the_number()

def madlibs():
    madlibs_game()
    
def handle_games():
    games = ["guess_the_number", "madlibs"]
    x = random.choice(games)
    if x == "guess_the_number":
        guess_game()
    elif x == "madlibs":
        madlibs()


def run_maggie():
    while True:
        user_input = take_command()
        response = generate_response(user_input)
        talk(response)

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

run_maggie()

