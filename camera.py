import cv2
from picamera2 import Picamera2
picam=Picamera2()
picam.preview_configuration.main.size=(300,300)
picam.preview_configuration.main.format="RGB888"
picam.preview_configuration.align()
picam.configure("preview")
picam.start()
while True:
        frame=picam.capture_array()
        cv2.imshow("picam",frame)
        if cv2.waitKey(1)==ord('q'):
                picam.capture_file('/home/pi/Desktop/Anu.jpg')
                break
cv2.destroyAllWindows()
