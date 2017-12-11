from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/home')
def home():
    return render_template('WeatherHome.html')


if __name__ == '__main__':
    app.run()
