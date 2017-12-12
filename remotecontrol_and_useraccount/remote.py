from flask import Flask, render_template, request, session, redirect, url_for
from forms import SignupForm, LoginForm, DeviceForm
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

device_type_dict = {}

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

    device_types = ['light', 'fan', 'TV', 'AC', 'device']
    brands = ['Samsung', 'LG', 'Sony', 'Philips', 'Panasonic', 'Xiaomi', 'Hitachi', 'Fujitsu', 'Sharp', 'Toshiba']

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

    device_name_dict = {}
    device_settings_dict = {}
    device_dict = {}
    device_power = {}

    if dictionary is not None:
        device_dict = dictionary.items()

        for device_type, devices in device_dict:
            device_names = []

            for name, settings in devices.items():
                device_names.append(name)

                device_settings_dict[name] = {}

                for key, val in settings.items():
                    device_settings_dict[name][key] = val

                device_power[name] = device_settings_dict[name]['power']

                global device_type_dict
                device_type_dict[name] = device_type

            device_name_dict[device_type] = device_names


    return render_template('remote_devices.html', brands=brands, device_types=device_types, form=form, device_dict=device_dict, device_name_dict=device_name_dict, device_settings_dict=device_settings_dict, device_power=device_power)

@app.route('/remote/power', methods=['POST'])
def power():
    device_name = request.form['name']
    device_power = request.form['power']

    user_remote_ref = user_ref.child('remote')
    user_devices_ref = user_remote_ref.child('devices')
    user_device_type_ref = user_devices_ref.child(device_type_dict[device_name])

    user_device_type_ref.update({
        device_name+'/power': device_power
    })

    return 'nothing'

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
