import datetime
import os
import pyttsx3
import speech_recognition as sr
import eel
import wikipedia
import pygame

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing....')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language = 'en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
    except:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):

    if message == 1:
       query = takecommand()
       print(query)
       eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:

       if "open" in query:
            from engine.features import openCommand
            openCommand(query)

       elif "on youtube" in query:
           from engine.features import PlayYoutube
           PlayYoutube(query)

       elif 'the time' in query:
           strTime = datetime.datetime.now().strftime("%I:%M:%p")
           print(strTime)
           speak(f"Sir, the time is {strTime}")
      
       elif 'tell me about' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            speak(results)

       elif 'play video' in query:
            video_dir = 'F:\\Images\\videos'
            video = os.listdir(video_dir)
            speak("Playing video....")
            os.startfile(os.path.join(video_dir, video[0]))

       elif 'play music' in query:
            from engine.features import PlayRandomMusic
            PlayRandomMusic()

       elif 'stop the music' in query:
           pygame.mixer.music.stop()
           speak("Sir, the music has been stopped.")

       elif 'joke' in query:
            from engine.features import jokes
            jokes()

       elif 'take a screenshot' in query:
           from engine.features import screenshot
           screenshot()
                
       else:
           print("not run")
    except:
        print("error")

    eel.ShowHood()