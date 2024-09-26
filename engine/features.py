import shlex
import struct
import time
from engine.helper import extract_yt_term
import pyaudio
import pyautogui
from engine.db import sqlite3
import webbrowser
import pvporcupine
from playsound import playsound 
import eel
from engine.config import ASSISTANT_NAME
from engine.command import speak
import os
import pygame
import random
import pywhatkit as kit
import pyjokes

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "").strip().lower()

    if query:
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name =?', (query,))
            results = cursor.fetchall()

            if results:
                speak(f"Opening {query}")
                os.startfile(results[0][0])
            else:
                cursor.execute('SELECT url FROM web_command WHERE name =?', (query,))
                results = cursor.fetchall()

                if results:
                    speak(f"Opening {query}")
                    webbrowser.open(results[0][0])    
                else:
                    speak(f"Opening {query}")
                    try:
                        os.system(f'start {shlex.quote(query)}')
                    except Exception as e:
                        speak("Not found")
                        print(e)
        except Exception as e:
            speak("Something went wrong")
            print(e)

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak(f"Playing {search_term} on YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Pre-trained keywords
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)

        # Loop for streaming
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            # Processing keyword from mic
            keyword_index = porcupine.process(keyword)

            # Checking if a keyword was detected
            if keyword_index >= 0:
                print("Hotword detected")

                # Pressing shortcut key Win+J
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")
                
    except Exception as e:
        print(e)
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def PlayRandomMusic():
   pygame.mixer.init()
   music_directory = 'C:\\Users\\cnb\\Music\\Music\\BGM theme'
   all_files = os.listdir(music_directory)
   music_files = [file for file in all_files if file.endswith(('.mp3', '.wav'))]
   if music_files:
      random_file = random.choice(music_files)
      random_file_path = os.path.join(music_directory, random_file)
      pygame.mixer.music.load(random_file_path)
      speak("Playing music....")
      pygame.mixer.music.play()

   else:
    print("No music files found in the directory.")

def jokes():
    my_jokes = pyjokes.get_joke('en')
    print(my_jokes)
    speak(my_jokes)

def screenshot():
    img = pyautogui.screenshot()
    img.save("C:\\Users\\cnb\\Documents\\Jarvis\\jarvis_img\\js.png")
    speak("I have taken the screenshot.")


