from flask import Flask, render_template, request
from firebase_admin import credentials, db
from win10toast import ToastNotifier
import requests
import firebase_admin

cred = credentials.Certificate("cred/ooppgroup4-firebase-adminsdk-vr92m-06ddf6875d.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ooppgroup4.firebaseio.com/'
})

app = Flask(__name__)

app.secretkey = 'oopp2017group4'


@app.route("/WeatherHome")
def weatherHome():
    return render_template("WeatherHome.html")

@app.route("/WeatherStart")
def weatherStart():
    return render_template("WeatherStart.html")

@app.route('/WeatherSettings', methods=['POST'])
def weathntempsettings():
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
                "Closing your windows...",
                duration=5)
            toaster.show_toast(
                "Closed Windows",
                "Your windows are now closed",
                icon_path=None,
                duration=5,
                threaded=True
            )
        elif weather == "Clouds":
            toaster = ToastNotifier()
            toaster.show_toast(
                "Clear weather",
                "Opening your windows...",
                duration=5)
            toaster.show_toast(
                "Opened Windows",
                "Your windows are now open.",
                icon_path=None,
                duration=5,
                threaded=True
                )
        return render_template('WeatherSettings.html', temp=temp_c, humid=humidity, windspd=wind_speed, weath=weather, descrip=weather_descrip)



if __name__ == '__main__':
    app.run(debug=True)


