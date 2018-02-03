from flask import Flask, render_template, request, session, redirect, url_for
from firebase_admin import credentials, db
from win10toast import ToastNotifier
import requests
import firebase_admin
from forms import SignupForm, LoginForm
from werkzeug import generate_password_hash, check_password_hash

cred = credentials.Certificate("cred/ooppgroup4-firebase-adminsdk-vr92m-06ddf6875d.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ooppgroup4.firebaseio.com/'
})

app = Flask(__name__)

app.secret_key = 'oopp2017group4'


@app.route("/WeatherHome")
def weatherHome():
    # Check if user is NOT logged in
    if 'email' in session:
        return redirect(url_for('weatherStart'))
    ###########################

    return render_template("WeatherHome.html")

@app.route("/WeatherStart")
def weatherStart():
    # Check if user is logged in
    if 'email' not in session:
        return redirect(url_for('login'))
    ###########################

    return render_template("WeatherStart.html")

@app.route('/WeatherSettings', methods=['POST'])
def weathntempsettings():
        #Check if user is logged in
        if 'email' not in session:
            return redirect(url_for('login'))
        ###########################

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
        return render_template('WeatherSettings.html', temp=temp_c, humid=humidity, windspd=wind_speed, weath=weather, descrip=weather_descrip)

#Signup, Login, and Logout

ref = db.reference()
users_ref = ref.child('users')
user_ref = ''

@app.before_first_request
def reset_session():
    session.pop('email', None)

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

#Temporary index page (logged out)
@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('home'))

    loginform = LoginForm(prefix='login')
    signupform = SignupForm(prefix='signup')

    return render_template('index.html', loginform=loginform, signupform=signupform)

#Temporary home page (logged in)
@app.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('index'))

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)


