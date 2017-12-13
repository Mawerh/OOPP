import speech_recognition as sr
from gtts import gTTS
import os
from time import ctime
import time
import wikipedia
from playsound import playsound
from mutagen.mp3 import MP3



def recordAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        #tts = gTTS(text="Say something.", lang='en')
        #tts.save('sound.mp3')
        #playsound('C:\\Users\\Ho Joey\\Documents\\GitHub\\OOPP\\voice_control1\\sound.mp3')
        #mp3 = MP3('sound.mp3')
        #mp3.delete()
        audio = r.listen(source)
    data = ''
    try:
        data = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data


def vision(data):
    if "how are you" in data:
        tts = gTTS(text="I am fine sir thank you.", lang='en')
        tts.save('sound.mp3')

    elif "what time is it" in data:
        tts = gTTS(text=ctime(), lang='en')
        tts.save('sound.mp3')

    elif "your name" in data:
        tts = gTTS(text="My name is Vision sir, and I am built to serve you.", lang='en')
        tts.save('sound.mp3')

    elif "where is" in data:
        data = data.split(" ")
        meaning = data[2]
        info = wikipedia.summary(meaning, sentences=2)
        tts = gTTS(text= info, lang='en')
        tts.save('sound.mp3')
        #os.system("chrome https://www.google.com.sg/maps/" + location)

    elif "turn on" in data:
        data = data.split(" ")
        device = data[2]
        tts = gTTS(text='Yes sir. Initializing interface. Turning on ' + device, lang='en')
        tts.save('sound.mp3')


    else:
        tts = gTTS(text='Sorry sir, I did not catch that.', lang='en')
        tts.save('sound.mp3')

