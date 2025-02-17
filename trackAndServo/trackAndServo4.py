import cv2
import time
import pantilthat
import numpy as np

from picamera2 import Picamera2
from libcamera import Transform

# Global vars
dispW = 640
dispH = 360

fps = 0
fps_text_position = (10,15)
fps_text_font = cv2.FONT_HERSHEY_SIMPLEX
fps_text_height = 0.5
fps_text_color = (0,0,255)
fps_text_weight = 1

dist_text_position = (80,15)

hueLow = 0
hueHigh = 0
satLow = 0
satHigh = 0
valLow = 0
valHigh = 0
track = 0
reset = 0
zoomTrack = 0

#Define object specific variables  
dist = 0
focal = 760
pixels = 55
width = 10 # Specifically for tennis ball

# set start up servo positions
panError = 0
tiltError = 0
panAngle = 0
tiltAngle = 0
pantilthat.pan(panAngle)
pantilthat.tilt(tiltAngle)

aAverage = 0
zoomCont = 0

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
              
def onTrack7(val):
    global track
    track = val
    
def onTrack8(val):
    global focal
    focal = val
    
def onTrack9(val):
    global reset
    reset = val
    
def onTrack10(val):
    global zoomTrack
    zoomTrack = val
    
    
#find the distance from then camera
def get_dist(pixels):
    dist  = (width*focal)/pixels
    return dist
    
cv2.namedWindow('myTracker')

cv2.createTrackbar('Hue Low', 'myTracker', 29, 179, onTrack1)
cv2.createTrackbar('Hue High', 'myTracker', 39, 179, onTrack2)
cv2.createTrackbar('Sat Low', 'myTracker', 202, 255, onTrack3)
cv2.createTrackbar('Sat High', 'myTracker', 255, 255, onTrack4)
cv2.createTrackbar('Val Low', 'myTracker', 51, 255, onTrack5)
cv2.createTrackbar('Val High', 'myTracker', 255, 255, onTrack6)
cv2.createTrackbar('Train', 'myTracker', 0, 1, onTrack7)
#cv2.createTrackbar('Focal Lenght', 'myTracker', 760, 1000, onTrack8)
cv2.createTrackbar('Reset', 'myTracker', 0, 1, onTrack9)
cv2.createTrackbar('Zoom', 'myTracker', 0, 1, onTrack10)

# Camera Settings
piCam = Picamera2()
piCam.preview_configuration.main.size=(dispW, dispH)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.transform=Transform(vflip=1, hflip=1)
piCam.preview_configuration.controls.FrameRate=30
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

zoomSize = piCam.capture_metadata()['ScalerCrop'][2:]
originalW = zoomSize[0] # 1920
originalH = zoomSize[1] # 1080
full_res = piCam.camera_properties['PixelArraySize']

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
    
    contours, junk = cv2.findContours(myMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contours =  sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
        #cv2.drawContours(frame, contours,  0, (255, 0, 0), 3)
        contour = contours[0]
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 3)
        area = w*h
        aAverage = .9*aAverage + .1*area

        print("zoomSize: " + str(zoomSize))
        print()
        
        if reset == 1:
            panAngle = 0
            tiltAngle = 0
            pantilthat.pan(panAngle)
            pantilthat.tilt(panAngle)
            
        if zoomTrack == 1:
            #print("AAverage: " + str(int(aAverage)))
            
            # TODO: Missing maximum zoom in
            if aAverage < 500 and area > 50:
                zoomSize = [int(s * 0.99) for s in zoomSize]
                offset = [(r - s) // 2 for r, s in zip(full_res, zoomSize)]
                piCam.set_controls({"ScalerCrop": offset + zoomSize})
            
            if aAverage > 1000 and (zoomSize[0] < originalW or zoomSize[1] < originalH):
                #zoomSize = [int(s + (s * 0.01)) for s in zoomSize]
                if zoomSize[0] < originalW:
                    zoomW = int(zoomSize[0] + (zoomSize[0] * 0.01))
                else:
                    zoomW = 1920
                if zoomSize[1] < originalH:
                    zoomH = int(zoomSize[1] + (zoomSize[1] * 0.01))
                else:
                    zoomH = 1080
                zoomSize = [zoomW, zoomH]
                offset = [(r - s) // 2 for r, s in zip(full_res, zoomSize)]
                piCam.set_controls({"ScalerCrop": offset + zoomSize})

        if track == 1 and reset == 0 and area > 50:
            distancia = get_dist(w)
            cv2.putText(frame, str(int(distancia)) + "cm", dist_text_position, fps_text_font, fps_text_height, fps_text_color, fps_text_weight)
            
            panCalc = (x+w/2)-dispW/2
            if panCalc > panError + 5 or panCalc < panError - 5:
                panError = panCalc
                panAngle = panAngle - panError/75
                
                if panAngle <-90:
                    panAngle=-90
                if panAngle >90:
                    panAngle=90
                if abs(panError) > 35:
                    pantilthat.pan(panAngle)
            
            tiltCalc = (y+h/2)-dispH/2
            if tiltCalc > tiltError + 5 or tiltCalc < tiltError - 5:
                tiltError = tiltCalc
                tiltAngle = tiltAngle + tiltError/75
                
                if tiltAngle <-90:
                    tiltAngle=-90
                if tiltAngle >40:
                    tiltAngle=40
                if abs(tiltError) > 35:
                    pantilthat.tilt(tiltAngle)

    # --- End of Frame logic
    cv2.putText(frame, str(int(fps)) + " fps", fps_text_position, fps_text_font, fps_text_height, fps_text_color, fps_text_weight)
    cv2.imshow("Camera", frame)
    cv2.imshow("My Mask", myMaskSmall)
#     cv2.imshow("Object of Interest", objectOfInterestSmall)
    
    if cv2.waitKey(1) == ord('q'):
        break
    
    time_end = time.time()
    loop_time = time_end - time_start
    fps = .9*fps + .1*(1/loop_time)

cv2.destroyAllWindows()
