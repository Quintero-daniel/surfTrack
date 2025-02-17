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

hueLow = 0
hueHigh = 0
satLow = 0
satHigh = 0
valLow = 0
valHigh = 0

def onTrack1(val):
    global hueLow
    hueLow = val
    
def onTrack2(val):
    global hueHigh
    hueHigh = val
    
def onTrack3(val):
    global satLow
    satLow = val
    
def onTrack4(val):
    global satHigh
    satHigh = val
    
def onTrack5(val):
    global valLow
    valLow = val
    
def onTrack6(val):
    global valHigh
    valHigh = val
    
cv2.namedWindow('myTracker')

cv2.createTrackbar('Hue Low', 'myTracker', 0, 179, onTrack1)
cv2.createTrackbar('Hue High', 'myTracker', 0, 179, onTrack2)
cv2.createTrackbar('Sat Low', 'myTracker', 100, 255, onTrack3)
cv2.createTrackbar('Sat High', 'myTracker', 255, 255, onTrack4)
cv2.createTrackbar('Val Low', 'myTracker', 100, 255, onTrack5)
cv2.createTrackbar('Val High', 'myTracker', 255, 255, onTrack6)

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
    lowerBound = np.array([hueLow, satLow, valLow])
    upperBound = np.array([hueHigh, satHigh, valHigh])

    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
    myMaskSmall = cv2.resize(myMask, (int(dispH/2), int(dispH/2)))
    objectOfInterest = cv2.bitwise_and(frame, frame, mask=myMask)
    objectOfInterestSmall = cv2.resize(objectOfInterest, (int(dispH/2), int(dispH/2)))
    
    # --- End of Frame logic
    cv2.putText(frame, str(int(fps)), fps_text_position, fps_text_font, fps_text_height, fps_text_color, fps_text_weight)
    cv2.imshow("Camera", frame)
    cv2.imshow("My Mask", myMaskSmall)
    #cv2.imshow("Object of Interest", objectOfInterestSmall)
    
    if cv2.waitKey(1) == ord('q'):
        break
    
    time_end = time.time()
    loop_time = time_end - time_start
    fps = .9*fps + .1*(1/loop_time)

cv2.destroyAllWindows()
