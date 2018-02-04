from flask import Flask, render_template, redirect, request, flash, url_for
from voice_functions import *
import firebase_admin
from firebase_admin import credentials, db
from playsound import playsound
import os
import time
import pytz
import datetime
from time import gmtime, strftime
from gtts import gTTS
import webbrowser
from weather import Weather


cred = credentials.Certificate("cred/ooppgroup4-firebase-adminsdk-vr92m-06ddf6875d.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ooppgroup4.firebaseio.com/'
})

app = Flask(__name__)

app.secret_key = 'oopp2017group4'


@app.route('/voice/')
def page():
    commands_file = open('commands_history.txt', 'r')
    responses_file = open('responses_history.txt', 'r')

    commands_list = []
    count = 0

    for line in commands_file:
        commands_list.append(line)
        count += 1

    responses_list = []

    for line in responses_file:
        responses_list.append(line)

    commands_file.close()
    responses_file.close()

    return render_template('voice.html', commands_list=commands_list, responses_list=responses_list, count=count)


weather = Weather()


@app.route('/voice/function')
def call_function():
    start_up()
    vision(data=recordAudio())
    return redirect(url_for('page'))

def vision(data):

    if "weather" in data:
        global count_qns1
        lookup = weather.lookup(569829)
        condition = lookup.condition()
        print(condition.text())
        location = weather.lookup_by_location('yio chu kang')
        forecasts = location.forecast()
        low_f = int(forecasts[0].low())
        low_c = int((low_f - 32) * (5 / 9))
        high_f = int(forecasts[0].high())
        high_c = int((high_f - 32) * (5 / 9))
        response = 'The weather today is ' + condition.text() + ', with a high of ' + str(high_c) + ' degrees and a low of ' + str(low_c) + ' degrees.'
        tts = gTTS(response, lang='en')
        file = str(count_qns1) + 'sound1.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns1 += 1
        commands_file = open('commands_history.txt', 'a')
        responses_file = open('responses_history.txt', 'a')
        command = 'How is the weather today?'
        commands_file.write(command+'\n')
        responses_file.write(response+'\n')
        commands_file.close()
        responses_file.close()

    elif "time" in data:
        global count_qns2
        now = datetime.datetime.now()
        timee = datetime.time(now.hour, now.minute, now.second)
        response = "It is " + str(timee)
        tts = gTTS(response, lang='en')
        file = str(count_qns2) + 'sound2.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns2 += 1
        commands_file = open('commands_history.txt', 'a')
        responses_file = open('responses_history.txt', 'a')
        command = 'What time is it?'
        commands_file.write(command+'\n')
        responses_file.write(response+'\n')
        commands_file.close()
        responses_file.close()

    elif "date" in data:
        global count_qns11
        kl = pytz.timezone('Asia/Kuala_Lumpur')
        response = "It is " + str(strftime("%a %d %b %Y", gmtime()))
        tts = gTTS(response, lang='en')
        file = str(count_qns11) + 'sound11.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns11 += 1
        commands_file = open('commands_history.txt', 'a')
        responses_file = open('responses_history.txt', 'a')
        command = 'What is the date today?'
        commands_file.write(command + '\n')
        responses_file.write(response + '\n')
        commands_file.close()
        responses_file.close()

    elif "turn on" in data:
        global count_qns5
        data = data.split(" ")
        device = data[2:]
        device_str = " ".join(str(x) for x in device)
        response = "Turning on " + str(device_str)
        tts = gTTS(response, lang='en')
        file = str(count_qns5) + 'sound5.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns5 += 1
        commands_file = open('commands_history.txt', 'a')
        responses_file = open('responses_history.txt', 'a')
        data_str = " ".join(str(x) for x in data)
        command = data_str.upper()[0] + data_str[1:]
        commands_file.write(command + '\n')
        responses_file.write(response + '\n')
        commands_file.close()
        responses_file.close()

    elif "turn off" in data:
        global count_qns3
        data = data.split(" ")
        device = data[2:]
        response = "Turning off " + str(device)
        tts = gTTS(response, lang='en')
        file = str(count_qns3) + 'sound3.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns3 += 1
        commands_file = open('commands_history.txt', 'a')
        responses_file = open('responses_history.txt', 'a')
        data_str = " ".join(str(x) for x in data)
        command = data_str.upper()[0] + data_str[1:]
        commands_file.write(command + '\n')
        responses_file.write(response + '\n')
        commands_file.close()
        responses_file.close()

    elif "open the door" in data:
        global count_qns7
        response = "Opening the door"
        tts = gTTS(response, lang='en')
        file = str(count_qns7) + 'sound7.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns7 += 1
        commands_file = open('commands_history.txt', 'a')
        responses_file = open('responses_history.txt', 'a')
        command = "Open the door"
        commands_file.write(command + '\n')
        responses_file.write(response + '\n')
        commands_file.close()
        responses_file.close()

    elif "close the door" in data:
        global count_qns8
        response = "Closing the door"
        tts = gTTS(response, lang='en')
        file = str(count_qns8) + 'sound8.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns8 += 1
        commands_file = open('commands_history.txt', 'a')
        responses_file = open('responses_history.txt', 'a')
        command = "Close the door"
        commands_file.write(command + '\n')
        responses_file.write(response + '\n')
        commands_file.close()
        responses_file.close()

    elif "search for" in data:
        global count_qns14
        data = data.split(" ")
        search = data[2:]
        response = 'Carrying out task'
        tts = gTTS(response, lang='en')  # have a function that types in the wanted search for users
        webbrowser.open('https://www.google.com.sg' + '\/search?q=' + str(search))  # Go to google
        file = str(count_qns14) + 'sound14.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns14 += 1
        commands_file = open('commands_history.txt', 'a')
        responses_file = open('responses_history.txt', 'a')
        command = "Search for " + str(search)
        commands_file.write(command + '\n')
        responses_file.write(response + '\n')
        commands_file.close()
        responses_file.close()

    elif "I would like to do some shopping" in data:
        global count_qns15
        webbrowser.open('https://www.amazon.com')
        response = 'Redirecting'
        tts = gTTS(response, lang='en')
        file = str(count_qns15) + 'sound15.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns15 += 1
        commands_file = open('commands_history.txt', 'a')
        responses_file = open('responses_history.txt', 'a')
        command = 'I would like to do some shopping'
        commands_file.write(command + '\n')
        responses_file.write(response + '\n')
        commands_file.close()
        responses_file.close()

    elif "how are my friends doing" in data:
        global count_qns16
        response = 'On it sir, let\'s see what your friends are up to.'
        tts = gTTS(response, lang='en')
        file = str(count_qns16) + 'sound16.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        webbrowser.open('https://www.facebook.com')
        count_qns16 += 1
        commands_file = open('commands_history.txt', 'a')
        responses_file = open('responses_history.txt', 'a')
        command = 'I would like to do some shopping'
        commands_file.write(command + '\n')
        responses_file.write(response + '\n')
        commands_file.close()
        responses_file.close()

    else:
        global count_qns6
        tts = gTTS(text='Sorry sir, I did not catch that.', lang='en')
        file = str(count_qns6) + 'sound6.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        count_qns6 += 1


def start_up():
    global count_qns10
    time.sleep(1)
    tts = gTTS(text='Greeting master, what can I do for you?', lang='en')
    file = str(count_qns10) + 'sounds.mp3'
    tts.save(file)
    playsound(file)
    os.remove(file)
    count_qns10 += 1



if __name__ == '__main__':
    app.run(debug=True)