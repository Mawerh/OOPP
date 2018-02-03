from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/Homepage")
def HomepageStart():

    return render_template("Homepage.html")

if __name__ == '__main__':
    app.run(debug=True)
