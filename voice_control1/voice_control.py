from flask import Flask, render_template, redirect
from voice_functions import *

app = Flask(__name__)

#allow user to input commands as well

@app.route('/voice')
def page():
    return render_template('voice.html')

@app.route('/voice/function')
def call_function():
    vision(data=recordAudio())
    return playsound('C:\\Users\\Ho Joey\\Documents\\GitHub\\OOPP\\voice_control1\\sound.mp3')


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
    app.run(debug=True)
