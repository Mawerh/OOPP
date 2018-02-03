from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/Homepage")
def homepageStart():
   return render_template("Homepage.html")

if __name__ == '__main__':
    app.run(debug=True)
