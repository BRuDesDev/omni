import subprocess
from gtts import gTTS
import os

myTTS = "Hello Master... Are you my .... father?"


def speak_text(text):
    filename = "test.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

    subprocess.run(["afplay", filename])

    os.remove(filename)


if __name__ == "__main__":
    speak_text(myTTS)