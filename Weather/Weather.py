from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/WeatherSettings')

def settings():
    city = "Singapore"
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=53e032f7efd36727cf5fa955bb4ffeb1")
    json_object = r.json()
    Weather = str(json_object["weather"]["main"])
    WeatherDescription = str(json_object["weather"]["description"])
    return render_template('WeatherSettings.html', weath=Weather, descrip=WeatherDescription)

@app.route("/WeatherHome")
def home():
    return render_template("WeatherHome.html")

if __name__ == '__main__':
    app.run(debug=True)
