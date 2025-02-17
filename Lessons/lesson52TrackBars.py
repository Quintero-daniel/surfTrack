import cv2
import time
import numpy as np

from picamera2 import Picamera2

# Global vars
dispW = 640
dispH = 360

fps = 0
fps_text_position = (10,30)
fps_text_font = cv2.FONT_HERSHEY_SIMPLEX
fps_text_height = 0.5
fps_text_color = (0,0,255)
fps_text_weight = 1

hueLow = 170
hueHigh = 180

satLow = 100
satHigh = 255

valLow = 100
valHigh = 255

lowerBound = np.array([hueLow, satLow, valLow])
upperBound = np.array([hueHigh, satHigh, valHigh])

# Camera Settings
piCam = Picamera2()
piCam.preview_configuration.main.size=(dispW, dispH)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.controls.FrameRate=30
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

while True:
    time_start = time.time()
    frame = piCam.capture_array()
    # --- Frame Logic
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
    myMaskSmall = cv2.resize(myMask, (int(dispH/2), int(dispH/2)))
    objectOfInterest = cv2.bitwise_and(frame, frame, mask=myMask)
    objectOfInterestSmall = cv2.resize(objectOfInterest, (int(dispH/2), int(dispH/2)))
    
    print(frameHSV[int(dispH/2), int(dispW/2)])
    # --- End of Frame logic
    cv2.putText(frame, str(int(fps)), fps_text_position, fps_text_font, fps_text_height, fps_text_color, fps_text_weight)
    cv2.imshow("Camera", frame)
    cv2.imshow("My Mask", myMaskSmall)
    cv2.imshow("Object of Interest", objectOfInterestSmall)
    
    if cv2.waitKey(1) == ord('q'):
        break
    
    time_end = time.time()
    loop_time = time_end - time_start
    fps = .9*fps + .1*(1/loop_time)

cv2.destroyAllWindows()
