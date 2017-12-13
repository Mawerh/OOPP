import speech_recognition as sr
from gtts import gTTS
import os
from time import ctime
import time
import wikipedia
from playsound import playsound
from mutagen.mp3 import MP3
import pygame as pg
from tempfile import TemporaryFile
from weather import Weather


def recordAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    data = ''
    try:
        data = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data


count_qns1 = 0
count_qns2 = 0
count_qns3 = 0
count_qns4 = 0
count_qns5 = 0
count_qns6 = 0

weather = Weather()

def vision(data):
    if "how is the weather" in data:
        global count_qns1
        lookup = weather.lookup(569829)
        condition = lookup.condition()
        location = weather.lookup_by_location('yio chu kang')
        forecasts = location.forecast()
        low_f = int(forecasts[0].low())
        low_c = int((low_f - 32) * (5 / 9))
        high_f = int(forecasts[0].high())
        high_c = int((high_f - 32) * (5 / 9))
        tts = gTTS(text='The weather today is' + condition.text() + ', with a high of' +str(high_c)+'degrees and a low of' + str(low_c) + 'degrees', lang='en')
        file = str(count_qns1) + 'sound1.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns1 += 1

    elif "what time is it" in data:
        global count_qns2
        tts = gTTS(text=ctime(), lang='en')
        file = str(count_qns2) + 'sound2.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns2 += 1

    #elif "" in data:
     #   global count_qns3
      #  tts = gTTS(text='It takes approximately' , lang='en')
       # file = str(count_qns3) + 'sound3.mp3'
        #tts.save(file)
        #playsound(file)
        #os.remove(file)
        #count_qns3 += 1

    elif "where is" in data:
        global count_qns4
        data = data.split(" ")
        meaning = data[2]
        info = wikipedia.summary(meaning, sentences=2)
        tts = gTTS(text=info, lang='en')
        file = str(count_qns4) + 'sound4.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns4 += 1
        #os.system("chromium-browser https://www.google.nl/maps/place/" + meaning + "/&amp;")

    elif "turn on" in data:
        global count_qns5
        data = data.split(" ")
        device = data[2]
        tts = gTTS(text="Turning on " + device, lang='en')
        file = str(count_qns5) + 'sound5.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns5 += 1

    else:
        global count_qns6
        tts = gTTS(text='Sorry sir, I did not catch that.', lang='en')
        file = str(count_qns6) + 'sound6.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns6 += 1