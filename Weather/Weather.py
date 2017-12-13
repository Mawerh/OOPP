from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def WeatherHome():
    return render_template("WeatherHome.html")

@app.route('/WeatherSettings')
def WeatherSettings():
    return render_template("WeatherSettings.html")

if __name__ == '__main__':
    app.run()
