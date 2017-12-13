from flask import Flask, render_template, request, session, redirect, url_for
from forms import SignupForm, LoginForm, DeviceForm
from werkzeug import generate_password_hash, check_password_hash

import firebase_admin
from firebase_admin import credentials, db

from voice_functions import *

import requests

app = Flask(__name__)

#***START OF YEE LEI'S CODE***

cred = credentials.Certificate("cred/ooppsmartliving-firebase-adminsdk-wchbx-6f20b0e93f.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ooppsmartliving.firebaseio.com/'
})

ref = db.reference()
users_ref = ref.child('users')
user_ref = ''

device_types = ['light', 'fan', 'TV', 'AC', 'device']
brands = ['Samsung', 'LG', 'Sony', 'Philips', 'Panasonic', 'Xiaomi', 'Hitachi', 'Fujitsu', 'Sharp', 'Toshiba']

device_type_dict = {}

device_name_dict = {}
device_settings_dict = {}
device_dict = {}
device_power_dict = {}
device_brand_dict = {}

app.secret_key = 'oopp2017group4'

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('page'))

    loginform = LoginForm(prefix='login')
    signupform = SignupForm(prefix='signup')

    return render_template('login.html', loginform=loginform, signupform=signupform)

@app.route('/remote', methods=['GET', 'POST'])
def remote_devices():
    if 'email' not in session:
        return redirect(url_for('login'))

    form = DeviceForm()

    user_remote_ref = user_ref.child('remote')
    user_devices_ref = user_remote_ref.child('devices')

    if request.method == 'POST':
        if form.validate():
            device_brand = request.form['device_brand']
            device_type = request.form['device_type']
            device_name = form.name.data

            user_device_type_ref = user_devices_ref.child(device_type)

            user_device_type_ref.update({
                device_name+'/brand': device_brand,
                device_name+'/power': 'off'
            })


    dictionary = user_devices_ref.get()

    global device_type_dict

    global device_name_dict
    global device_settings_dict
    global device_dict
    global device_power_dict
    global device_brand_dict

    device_type_dict = {}

    device_name_dict = {}
    device_settings_dict = {}
    device_dict = {}
    device_power_dict = {}
    device_brand_dict = {}

    if dictionary is not None:
        device_dict = dictionary.items()

        for device_type, devices in device_dict:
            device_names = []

            for name, settings in devices.items():
                device_names.append(name)

                device_settings_dict[name] = {}

                for key, val in settings.items():
                    device_settings_dict[name][key] = val

                device_type_dict[name] = device_type
                device_power_dict[name] = device_settings_dict[name]['power']
                device_brand_dict[name] = device_settings_dict[name]['brand']

            device_name_dict[device_type] = device_names


    return render_template('remote_devices.html', brands=brands, device_types=device_types, form=form, device_dict=device_dict, device_name_dict=device_name_dict, device_settings_dict=device_settings_dict, device_power_dict=device_power_dict, device_brand_dict=device_brand_dict)

@app.route('/remote/power', methods=['POST'])
def device_power():
    device_name = request.form['name']
    device_power = request.form['power']

    user_remote_ref = user_ref.child('remote')
    user_devices_ref = user_remote_ref.child('devices')
    user_device_type_ref = user_devices_ref.child(device_type_dict[device_name])

    user_device_type_ref.update({
        device_name+'/power': device_power
    })

    return 'nothing'

@app.route('/remote/remove', methods=['POST'])
def device_remove():
    device_name = request.form['name']

    user_remote_ref = user_ref.child('remote')
    user_devices_ref = user_remote_ref.child('devices')
    user_device_type_ref = user_devices_ref.child(device_type_dict[device_name])

    user_device_type_ref.child(device_name).delete()

    return redirect(url_for('remote_devices'))

@app.route('/remote/rooms')
def rooms():
    return render_template('remote_rooms.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('voice'))

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

            users_ref.push({
                'firstname': first_name,
                'lastname': last_name,
                'email': email,
                'password': password_hash
            })

            session['email'] = email
            return redirect(url_for('page'))
    elif request.method == 'GET':
        return render_template('signup.html', signupform=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('voice'))

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
                return redirect(url_for('page'))
            else:
                return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('login.html', loginform=form)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

#***END OF YEE LEI'S CODE***



#***START OF JOEY'S CODE***

@app.route('/voice')
def page():
    return render_template('voice.html')

@app.route('/voice/function')
def call_function():
    vision(data=recordAudio())
    return redirect(url_for('page'))

#***END OF JOEY'S CODE***


#***START OF JOHN'S CODE***

@app.route("/WeatherHome")
def weatherHome():
    return render_template("WeatherHome.html")

@app.route("/WeatherStart")
def weatherStart():
    return render_template("WeatherStart.html")

@app.route('/WeatherSettings', methods=['POST'])
def settings():
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Singapore,SG&appid=53e032f7efd36727cf5fa955bb4ffeb1")
    json_object = r.json()
    temp_k = float(json_object["main"]["temp"])
    humidity = float(json_object['main']['humidity'])
    wind_speed = float(json_object['wind']['speed'])
    weather = json_object['weather'][0]["main"]
    weather_descrip = json_object['weather'][0]["description"]
    temp_c = int(temp_k - 273.15)
    return render_template('WeatherSettings.html', temp=temp_c, humid=humidity, windspd=wind_speed, weath=weather, descrip=weather_descrip)

#***END OF JOHN'S CODE***



if __name__ == '__main__':
    app.run(debug=True)
