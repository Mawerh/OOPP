from flask import Flask, render_template

app = Flask(__name__)


@app.route('/voice')
def hello_world():
    return render_template('voice.html')


if __name__ == '__main__':
    app.run()
