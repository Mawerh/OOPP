from flask import Flask, render_template, request
from win10toast import ToastNotifier
import requests
import urllib
from firebase import firebase

firebase = firebase.FirebaseApplication('https://weather-9587a.firebaseio.com/', authentication ='AIzaSyCwYgi9FEXOS354qs3Zbyd-3PirZsjFHQU')


app = Flask(__name__)

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
        return render_template('WeatherSettings.html', temp=temp_c, humid=humidity, windspd=wind_speed, weath=weather, descrip=weather_descrip)

def mainpsisettings():
        file = urllib.request('http://api.nea.gov.sg/api/WebAPI/?dataset=psi_update&keyref=781CF461BB6606AD48001FDD2657FAF020F860C60A7F1824')
        reading = file.getElementsByTagName('reading')
        reading = [items.attributes['value'].value for items in reading if items.attributes['type'].value == "NPSI"]
        for items in reading:
            if items.attributes['type'].value == "NPSI":
                return render_template('WeatherSettings.html', items.attribute['value'].value)

def popupmsettings():
        toaster = ToastNotifier()
        toaster.show_toast(
            "Rain Warning!!!",
            "It is going to rain soon. Closing your windows",
            duration=10)
        toaster.show_toast(
            "Example two",
            "This notification is in it's own thread!",
            icon_path=None,
            duration=5,
            threaded=True
        )
        # Wait for threaded notification to finish
        while toaster.notification_active(): time.sleep(0.1)

if __name__ == '__main__':
    app.run(debug=True)


