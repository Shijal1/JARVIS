import speech_recognition as sr
import pyttsx3
import pymongo
import os
import webbrowser
import requests
import googleapiclient.discovery
import subprocess
import shutil
from bs4 import BeautifulSoup  # For web scraping

# Initialize MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["jarvis_db"]
collection = db["commands"]
image_collection = db["images"]  # Separate collection for images

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Your YouTube API Key
YOUTUBE_API_KEY = "AIzaSyC0-wcdXU5iQ8QBrc4GIRh4Y6atoqhFFb4"

# Image folder path (set absolute path)
IMAGE_FOLDER = r"C:\Users\Lenovo\OneDrive\python\JARVIS-Assistant\images"

# Ensure 'images' folder exists
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

def speak(text):
    """Convert text to speech"""
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice input and convert it to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower().strip()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        print("Could not request results. Check your internet connection.")
        return None

def search_web(query):
    """Search Google for a query"""
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    speak(f"Searching for {query} on Google...")
    webbrowser.open(search_url)

def download_image(query):
    """Download and save the first image from Google search"""
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        img_tags = soup.find_all("img")

        img_url = None
        for img in img_tags[1:]:  # Skip first as it's usually a logo
            if "http" in img.get("src", ""):
                img_url = img["src"]
                break

        if img_url:
            img_path = os.path.join(IMAGE_FOLDER, f"{query.replace(' ', '_')}.jpg")

            try:
                img_data = requests.get(img_url).content
                with open(img_path, "wb") as file:
                    file.write(img_data)
                print(f"✅ Image downloaded and saved at {img_path}")
                image_collection.insert_one({"query": query, "path": img_path})  # Store in MongoDB
                return img_path
            except Exception as e:
                print(f"❌ Error saving image: {e}")

    print("❌ No valid image found.")
    return None

def get_image(query):
    """Fetch image from MongoDB or download if not available"""
    speak(f"Searching for an image of {query}...")

    result = image_collection.find_one({"query": query})

    if result:
        image_path = result["path"]
        if os.path.exists(image_path):  
            speak(f"Opening saved image of {query}.")
            os.startfile(image_path)
        else:
            speak("The image file is missing. Downloading again...")
            new_path = download_image(query)
            if new_path and os.path.exists(new_path):
                os.startfile(new_path)
            else:
                speak("I couldn't retrieve the image.")
    else:
        speak(f"Downloading an image of {query}...")
        image_path = download_image(query)

        if image_path and os.path.exists(image_path):
            speak("Here is the image.")
            os.startfile(image_path)
        else:
            speak("Sorry, I couldn't find an image.")

def play_music(song_name):
    """Search YouTube using API and play the first result"""
    speak(f"Searching YouTube for {song_name}...")

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    request = youtube.search().list(
        part="snippet",
        q=song_name,
        type="video",
        maxResults=1
    )
    response = request.execute()

    if response["items"]:
        video_id = response["items"][0]["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        collection.insert_one({"command": f"play music {song_name}", "youtube_url": video_url})

        speak("Playing your song now.")
        webbrowser.open(video_url)  
    else:
        speak("Sorry, I couldn't find that song.")

def get_my_location():
    """Get the user's current location"""
    try:
        response = requests.get("https://ipinfo.io/json").json()
        city = response.get("city", "Unknown city")
        region = response.get("region", "Unknown region")
        country = response.get("country", "Unknown country")

        location = f"You are in {city}, {region}, {country}."
        speak(location)
        print(location)
    except Exception as e:
        speak("I couldn't retrieve your location.")
        print(f"Error fetching location: {e}")

def search_location(place):
    """Open Google Maps for the requested location"""
    speak(f"Searching for {place} on Google Maps.")
    url = f"https://www.google.com/maps/search/{place.replace(' ', '+')}"
    webbrowser.open(url)

# Start JARVIS
speak("Hello, I am JARVIS. Say 'Hey JARVIS' to activate me.")

while True:
    wake_command = listen()
    if wake_command and "hey jarvis" in wake_command:
        speak("Yes, I am listening.")
        command = listen()

        if command:
            if command in ["where am i", "what is my location"]:
                get_my_location()
            elif command.startswith("search location for"):
                place = command.replace("search location for", "").strip()
                search_location(place)
            elif command.startswith("search for"):
                query = command.replace("search for", "").strip()
                search_web(query)
            elif command.startswith("play music"):
                song_name = command.replace("play music", "").strip()
                play_music(song_name)
            elif command.startswith("give me image of"):
                query = command.replace("give me image of", "").strip()
                get_image(query)
            else:
                speak("I don't know how to respond to that yet.")