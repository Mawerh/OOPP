from flask import Flask, render_template, redirect, request, flash, url_for
from voice_functions import *
import sys
import firebase_admin
from firebase_admin import credentials, db
import os


app = Flask(__name__)

#cred = credentials.Certificate('voice_control1/cred/voice-commands-6e0da-firebase-adminsdk-1oo8c-de3826367f.json')
#default_app = firebase_admin.initialize_app(cred, {
    #'databaseURL': 'https://voice-commands-6e0da.firebaseio.com/'
#})

#root = db.reference()


#allow user to input commands as well

@app.route('/voice')
def page():
    return render_template('voice.html')

@app.route('/voice/function')
def call_function():
    vision(data=recordAudio())
    return redirect(url_for('page'))





#greetings = recordAudio()
#tts = gTTS(text=greetings, lang='en')
#tts.save('sound.mp3')
#os.system('sound.mp3')
#while True:
#vision(data=recordAudio())
#playsound('C:\\Users\\Ho Joey\\Documents\\GitHub\\OOPP\\voice_control1\\sound.mp3')
#os.remove('sound.mp3')
#mp3 = MP3('sound.mp3')
#mp3.delete()




if __name__ == '__main__':
    #app.secret_key='Noona<3'
    app.run(debug=True)