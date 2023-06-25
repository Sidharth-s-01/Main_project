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
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
picam=Picamera2()
picam.preview_configuration.main.size=(300,300)
picam.preview_configuration.main.format="RGB888"
picam.preview_configuration.align()
picam.configure("preview")
picam.start()

GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def getDistance():

    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance




path="images"
images=[]
classNames =[]
myList=os.listdir(path)
PIR_PIN=17
GPIO.setup(PIR_PIN,GPIO.IN)

for cls in myList:
    currImg=cv2.imread(f'{path}/{cls}')
    images.append((currImg))
    classNames.append(os.path.splitext(cls)[0])

def findEncodings(images):
    encodeList=[]
    print("Starting to Encode all Images.....")
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        # faceLoc=face_recognition.face_locations(img)[0]
        encodeImg=face_recognition.face_encodings(img)[0]
        encodeList.append(encodeImg)
    print('Encoding Complete')
    return encodeList

encodeListForKnownFaces=findEncodings(images)


def VoiceRecognize():
    r=sr.Recognizer()
    r.energy_threshold = 500

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening....")
        audio= r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("Recognizing")
            return text
        except:
            print("sorry, could not recognise")

        

def face():
    picam.capture_file('test/test.jpg')
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
            cv2.waitKey(5000)
            cv2.destroyAllWindows()
            return name
    return "no_match"
    

    
while True:
    
    print("Application initializing.....")
    distance=getDistance()
    if distance<6:
        mytext = "Blockage Detected,stop stop stop"
                    
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=True)
        myobj.save("block.mp3")
        os.system("mpg321 block.mp3")
        continue
        
    word=VoiceRecognize()
    if word=="start":
        print("Starting")
        mytext2 = 'Starting Application'
        language = 'en'
        myobj2 = gTTS(text=mytext2, lang=language, slow=True)
        myobj2.save("starting.mp3")
        os.system("mpg321 starting.mp3")
        while True:
            print("Looking for motion and voice commands....")
            word2=VoiceRecognize()
            if GPIO.input(PIR_PIN)==GPIO.HIGH or word2=="hai" or word2=="identify":
                if GPIO.input(PIR_PIN)==GPIO.HIGH:

                    print("Motion Detected, Do you want me to Identify")
                    mytext1= 'Motion Detected, Do you want me to Identify'
                    language = 'en'
                    myobj1 = gTTS(text=mytext1, lang=language, slow=True)
                    myobj1.save("motion.mp3")
                    os.system("mpg321 motion.mp3")
                    while True:
                        word3=VoiceRecognize()
                        if word3=="yes":
                            print("Identifying Person")
                                                        
                            val=face()
                            if val=="no_match":
                                print("Could not identify person")
                                mytext = "Could not identify person"
                                language = 'en'
                                myobj = gTTS(text=mytext, lang=language, slow=True)
                                myobj.save("identify.mp3")
                                os.system("mpg321 identify.mp3")
                                break
                            else:
                                print("Suceessfully Identified person as: "+val)
                                mytext = "Successfully Identified person as: "+val
                                language = 'en'
                                myobj = gTTS(text=mytext, lang=language, slow=True)
                                myobj.save("identify.mp3")
                                os.system("mpg321 identify.mp3")
                        
                        
                                break
                
                        elif word3=="no":
                            print("Okey")
                            break
                        else:
                            continue
                    break
                elif word2=="identify":
                    print("starting to identify person....")
                    val=face()
                    if val=="no_match":
                        print("Could not identify person")
                        mytext = "Could not identify person "
                        language = 'en'
                        myobj = gTTS(text=mytext, lang=language, slow=True)
                        myobj.save("identify.mp3")
                        os.system("mpg321 identify.mp3")
                        break
                    else:
                        print("Successfully Identified person as: "+val)
                        mytext = "Successfully Identified person as: "+val
                        language = 'en'
                        myobj = gTTS(text=mytext, lang=language, slow=True)
                        myobj.save("identify.mp3")
                        os.system("mpg321 identify.mp3")
                        
                        break
                    
                elif word2=="hai":
                    print("starting to store person....")
                    mytext = 'Please wait two seconds and say your name'
                    language = 'en'
                    myobj = gTTS(text=mytext, lang=language, slow=True)
                    myobj.save("welcome.mp3")
                    os.system("mpg321 welcome.mp3")
                    while True:
                        name_of_person=VoiceRecognize()
                        if name_of_person=="":
                            continue
                        else:
                            break
                    print("Please speak anything")
                    picam.capture_file('images/'+name_of_person+'.jpg')
                    img=cv2.imread('images/'+name_of_person+'.jpg')
                    cv2.imshow(name_of_person, img)
                    cv2.waitKey(5000)
                    cv2.destroyAllWindows()
                    print("Successfully saved person as: "+name_of_person)
                    mytext = "Successfully saved person as: "+name_of_person
                    
                    language = 'en'
                    myobj = gTTS(text=mytext, lang=language, slow=True)
                    myobj.save("identify.mp3")
                    os.system("mpg321 identify.mp3")
                   
                    
                    print("Adding Picture to Encoding List....")
                    images=[]
                    for cls in myList:
                        currImg=cv2.imread(f'{path}/{cls}')
                        images.append((currImg))
                        classNames.append(os.path.splitext(cls)[0])
                    encodeListForKnownFaces=findEncodings(images)
                    break
                
                else:
                    continue
           
                
            
    elif word=="stop":
        continue
    
        



    
        


    

        
        

