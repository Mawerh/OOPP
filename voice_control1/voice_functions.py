import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound
from weather import Weather
import time
from time import ctime
import datetime
from time import gmtime, strftime
import pytz
import webbrowser

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
count_qns7 = 0
count_qns8 = 0
count_qns9 = 0
count_qns10 = 0
count_qns11 = 0
count_qns12 = 0
count_qns13 = 0
count_qns14 = 0
count_qns15 = 0
count_qns16 = 0
count_qns17 = 0