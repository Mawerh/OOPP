from flask import Flask, render_template, request, session, redirect, url_for
from forms import SignupForm, LoginForm, DeviceForm, RoomForm
from devices import Device
from werkzeug import generate_password_hash, check_password_hash

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("cred/ooppsmartliving-firebase-adminsdk-wchbx-6f20b0e93f.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ooppsmartliving.firebaseio.com/'
})

ref = db.reference()
users_ref = ref.child('users')
user_ref = ''

device_types = ['light', 'fan', 'TV', 'AC', 'device']
device_brands = ['Samsung', 'LG', 'Sony', 'Philips', 'Panasonic', 'Xiaomi', 'Hitachi', 'Fujitsu', 'Sharp', 'Toshiba', 'Dyson', 'Roomba']
device_locations = ['Bedroom', 'Living room', 'Balcony', 'Dining room', 'Kitchen', 'Toilet', 'Bathroom', 'Attic', 'Basement']

device_dict = {}

app = Flask(__name__)

app.secret_key = 'oopp2017group4'

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

@app.route('/remote', methods=['GET', 'POST'])
def remote_devices():
    if 'email' not in session:
        return redirect(url_for('login'))

    form = DeviceForm()

    user_remote_ref = user_ref.child('remote')
    user_devices_ref = user_remote_ref.child('devices')

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

    global device_dict
    device_dict = {}
    device_type_count = {}
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

            device_dict[device_type] = device_list

    for device_type in device_types:
        if device_type not in device_type_count:
            device_type_count[device_type] = 0

    return render_template('remote_devices.html', deviceform=form, device_types=device_types, device_brands=device_brands, device_locations=device_locations, device_dict=device_dict, device_type_count=device_type_count, device_count_range=device_count_range+1)

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

@app.route('/remote/rooms', methods=['GET', 'POST'])
def remote_rooms():
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
                'area': 0,
                'position_x': 0,
                'position_y': 0,
            })

    return render_template('remote_rooms.html', roomform=form)

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

            users_ref.push({
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

if __name__ == '__main__':
    app.run(debug=True)
