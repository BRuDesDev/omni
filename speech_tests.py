import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something...")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print(f"You said: {text}")
except sr.UnknownValueError:
    print("Didn't catch that.")
except sr.RequestError as e:
    print(f"Could not request results; {e}")
