import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
PIR_PIN=7
GPIO.setup(PIR_PIN,GPIO.IN)
while True:
    if GPIO.input(PIR_PIN)==GPIO.HIGH:
        print("Motion Detected")
        print("Turing Camera On")
        print(" ")
        time.sleep(2)
    else:
        print("No motion")
        print("Turing Camera off")
        time.sleep(2)
        
