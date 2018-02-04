from flask import Flask, render_template, request, session, redirect, url_for
from forms import SignupForm, LoginForm, DeviceForm, RoomForm
from remote_objects import Device, Room
from werkzeug import generate_password_hash, check_password_hash
from voice_functions import *
from playsound import playsound
import os
import time
import pytz
import datetime
from time import gmtime, strftime
from gtts import gTTS
import webbrowser
from weather import Weather
from win10toast import ToastNotifier
import requests

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("cred/ooppgroup4-firebase-adminsdk-vr92m-06ddf6875d.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ooppgroup4.firebaseio.com/'
})

ref = db.reference()
users_ref = ref.child('users')
user_ref = ''

device_types = ['light', 'fan', 'TV', 'AC', 'device']
device_brands = ['Samsung', 'LG', 'Sony', 'Philips', 'Panasonic', 'Mitsubishi', 'Xiaomi', 'Hitachi', 'Fujitsu', 'Sharp', 'Toshiba', 'Dyson', 'Roomba']
device_locations = ['Bedroom', 'Living room', 'Balcony', 'Dining room', 'Kitchen', 'Toilet', 'Bathroom', 'Attic', 'Basement']

device_dict = {}

app = Flask(__name__)

app.secret_key = 'oopp2017group4'

@app.before_first_request
def reset_session():
    session.pop('email', None)

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('home'))

    loginform = LoginForm(prefix='login')
    signupform = SignupForm(prefix='signup')

    return render_template('index.html', loginform=loginform, signupform=signupform)

@app.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('index'))

    return render_template('home.html')

### START OF YEE LEI'S REMOTE CONTROL, LOG IN, LOG OUT AND SIGN UP ###

@app.route('/remote', methods=['GET', 'POST'])
def remote_devices():
    if 'email' not in session:
        return redirect(url_for('login'))

    form = DeviceForm()

    user_remote_ref = user_ref.child('remote')
    user_devices_ref = user_remote_ref.child('devices')
    user_rooms_ref = user_remote_ref.child('rooms')

    if request.method == 'POST':
        if form.validate():
            device_type = request.form['device_type']
            device_brand = request.form['device_brand']
            device_location = request.form['device_location']
            device_name = form.name.data

            user_device_type_ref = user_devices_ref.child(device_type)

            user_device_type_ref.update({
                device_name+'/brand': device_brand,
                device_name+'/location': device_location,
                device_name+'/power': 'off'
            })

            user_room_ref = user_rooms_ref.child(device_location)

            user_room_ref.update({
                'length': 0,
                'width': 0,
                'position_x': 0,
                'position_y': 0,
            })

    global device_dict
    device_dict = {}
    device_type_count = {}
    device_location_list = []
    device_count_range = 0

    dictionary = user_devices_ref.get()

    if dictionary is not None:
        for device_type, devices in dictionary.items():
            device_list = []

            device_type_count[device_type] = len(devices)

            if device_count_range < len(devices):
                device_count_range = len(devices)

            for device_name, device_settings in devices.items():
                device_brand = device_settings['brand']
                device_power = device_settings['power']
                device_location = device_settings['location']

                device = Device(device_type, device_brand, device_name, device_location, device_power)
                device_list.append(device)

                if device_location not in device_location_list:
                    device_location_list.append(device_location)

            device_dict[device_type] = device_list

    for device_type in device_types:
        if device_type not in device_type_count:
            device_type_count[device_type] = 0

    return render_template('remote_devices.html', deviceform=form, device_types=device_types, device_brands=device_brands, device_locations=device_locations, device_dict=device_dict, device_type_count=device_type_count, device_count_range=device_count_range+1, device_location_list=device_location_list)

@app.route('/remote/power', methods=['POST'])
def remote_power():
    device_type = request.form['type']
    device_name = request.form['name']
    device_power = request.form['power']

    user_remote_ref = user_ref.child('remote')
    user_devices_ref = user_remote_ref.child('devices')
    user_device_type_ref = user_devices_ref.child(device_type)

    user_device_type_ref.update({
        device_name+'/power': device_power
    })

    return 'nothing'

@app.route('/remote/remove', methods=['POST'])
def device_remove():
    device_type = request.form['type']
    device_name = request.form['name']

    user_remote_ref = user_ref.child('remote')
    user_devices_ref = user_remote_ref.child('devices')
    user_device_type_ref = user_devices_ref.child(device_type)

    user_device_type_ref.child(device_name).delete()

    return redirect(url_for('remote_devices'))

@app.route('/remote/heatmap', methods=['GET', 'POST'])
def remote_heatmap():
    if 'email' not in session:
        return redirect(url_for('login'))

    form = RoomForm()

    user_remote_ref = user_ref.child('remote')
    user_rooms_ref = user_remote_ref.child('rooms')

    if request.method == 'POST':
        if form.validate():
            room_name = form.name.data

            user_room_ref = user_rooms_ref.child(room_name)

            user_room_ref.update({
                'name': room_name,
                'length': 0,
                'width': 0,
                'position_x': 0,
                'position_y': 0,
            })

    rooms_list = []

    dictionary = user_rooms_ref.get()

    if dictionary is not None:
        for room_name, room_config in dictionary.items():
            room_length = room_config['length']
            room_width = room_config['width']
            room_position_x = room_config['position_x']
            room_position_y = room_config['position_y']

            room = Room(room_name, room_length, room_width, room_position_x, room_position_y)

            rooms_list.append(room)

    return render_template('remote_heatmap.html', roomform=form, rooms_list=rooms_list)

@app.route('/remote/usage', methods=['GET', 'POST'])
def remote_usage():
    if 'email' not in session:
        return redirect(url_for('login'))

    return render_template('remote_usage.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))

    form = SignupForm(prefix='signup')

    if request.method == 'POST':
        if not form.validate():
            return render_template('signup.html', signupform=form)
        else:
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            password_hash = generate_password_hash(password)

            global user_ref
            user_ref = users_ref.push()
            user_ref.set({
                'firstname': first_name,
                'lastname': last_name,
                'email': email,
                'password': password_hash
            })

            session['email'] = email
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('signup.html', signupform=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))

    form = LoginForm(prefix='login')

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', loginform=form)
        else:
            email = form.email.data
            password = form.password.data

            user = users_ref.order_by_child('email').equal_to(email).get()

            validate_email = False
            for key, val in user.items():
                if val['email'] == email:
                    validate_email = True
                    global user_ref
                    user_ref = users_ref.child(key)

            if validate_email and check_password_hash(val['password'], password):
                session['email'] = email
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('login.html', loginform=form)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

### END OF YEE LEI'S REMOTE CONTROL, LOG IN, LOG OUT AND SIGN UP ###

### START OF JOEY'S VOICE CONTROL ###

@app.route('/voice/')
def voice_page():
    if 'email' not in session:
        return redirect(url_for('login'))

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
    if 'email' not in session:
        return redirect(url_for('login'))

    start_up()
    vision(data=recordAudio())
    return redirect(url_for('voice_page'))

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
    tts = gTTS(text='Greetings, what can I do for you?', lang='en')
    file = str(count_qns10) + 'sounds.mp3'
    tts.save(file)
    playsound(file)
    os.remove(file)
    count_qns10 += 1

### END OF JOEY'S VOICE CONTROL ###

### START OF JOHN'S WEATHER STATS AND WINDOW AUTOMATION ###

@app.route("/WeatherStart")
def weatherStart():
    if 'email' not in session:
        return redirect(url_for('login'))

    return render_template("WeatherStart.html")

@app.route('/WeatherSettings', methods=['POST'])
def weathntempsettings():
        if 'email' not in session:
            return redirect(url_for('login'))

        r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Singapore,SG&appid=53e032f7efd36727cf5fa955bb4ffeb1")
        json_object = r.json()
        temp_k = float(json_object["main"]["temp"])
        humidity = float(json_object['main']['humidity'])
        wind_speed = float(json_object['wind']['speed'])
        weather = json_object['weather'][0]["main"]
        weather_descrip = json_object['weather'][0]["description"]
        temp_c = int(temp_k - 273.15)
        if weather == "Rain":
            toaster = ToastNotifier()
            toaster.show_toast(
                "Rain Warning!!!",
                "Your windows are now closed",
                icon_path=None,
                duration=10,
                threaded=True
            )
        elif weather == "Clouds":
            toaster = ToastNotifier()
            toaster.show_toast(
                "Clear Weather",
                "Your windows are now open.",
                icon_path=None,
                duration=10,
                threaded=True
            )

        user_weather_ref = user_ref.child('weather')
        dictionary = user_weather_ref.get()

        return render_template('WeatherSettings.html', temp=temp_c, humid=humidity, windspd=wind_speed, weath=weather, descrip=weather_descrip, dictionary=dictionary)

@app.route('/WeatherSettings/setting', methods=['POST'])
def changewindowsettings():
    if 'email' not in session:
        return redirect(url_for('login'))

    setting = request.form['setting']
    switch = request.form['switch']

    user_weather_ref = user_ref.child('weather')

    user_weather_ref.update({
        setting: switch
    })

    return 'nothing'

### END OF JOHN'S WEATHER STATS AND WINDOW AUTOMATION ###

if __name__ == '__main__':
    app.run(debug=True)
