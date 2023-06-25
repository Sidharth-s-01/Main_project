

import speech_recognition as sr
import os

r=sr.Recognizer()
r.energy_threshold = 500

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    
    while True:
        print("Say anything : ")
        audio= r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("Recognizing")
            print("You said  :  "+text)
        except:
            print("sorry, could not recognise")

