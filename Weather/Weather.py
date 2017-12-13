from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def WeatherHome():
    return render_template("WeatherHome.html")

@app.route("/WeatherStart")
def WeatherStart():
    return render_template("WeatherStart.html")

@app.route('/WeatherSettings', methods=['POST'])
def home():
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Singapore,SG&appid=53e032f7efd36727cf5fa955bb4ffeb1")
    json_object = r.json()
    temp_k = float(json_object["main"]["temp"])
    humidity = float(json_object['main']['humidity'])
    wind_speed = float(json_object['wind']['speed'])
    weather = json_object['weather'][0]["main"]
    weather_descrip = json_object['weather'][0]["description"]
    temp_c = temp_k - 273.15
    return render_template('WeatherSettings.html', temp=temp_c, humid=humidity, windspd=wind_speed, weath=weather, descrip=weather_descrip)


if __name__ == '__main__':
    app.run(debug=True)
