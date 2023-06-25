
import cv2
import numpy as np
import face_recognition
import os
from gtts import gTTS

import RPi.GPIO as GPIO
import speech_recognition as sr

import time
import cv2
from picamera2 import Picamera2
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
picam=Picamera2()
picam.preview_configuration.main.size=(300,300)
picam.preview_configuration.main.format="RGB888"
picam.preview_configuration.align()
picam.configure("preview")
picam.start()


path="images"
images=[]
classNames =[]
myList=os.listdir(path)


for cls in myList:
    currImg=cv2.imread(f'{path}/{cls}')
    images.append((currImg))
    classNames.append(os.path.splitext(cls)[0])

def findEncodings(images):
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        # faceLoc=face_recognition.face_locations(img)[0]
        encodeImg=face_recognition.face_encodings(img)[0]
        encodeList.append(encodeImg)
    return encodeList

print("Starting to Encode all Images.....")
encodeListForKnownFaces=findEncodings(images)
print('Encoding Complete')
picam.capture_file('test/test.jpg')
print('Picture Taken')
            img=cv2.imread('test/test.jpg')
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            faceCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

            for encodeFace, faceloc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListForKnownFaces, encodeFace)
                face_dist = face_recognition.face_distance(encodeListForKnownFaces, encodeFace)
                print(face_dist)
                matchingIndex = np.argmin(face_dist)

                if matches[matchingIndex]:
                    name = classNames[matchingIndex].upper()
                    print(name)
                    cv2.imshow('webCam', img)
