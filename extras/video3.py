import cv2
import time
import pantilthat
import numpy as np

from datetime import datetime
from picamera2 import Picamera2, Preview
from libcamera import Transform
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

# Date and time
timeNow = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")).replace(" ", "")
videoNameAndFormat =  timeNow + '.mp4'

keyboardValue = ''
dispW = 640
dispH = 480

# Camera Settings
piCam = Picamera2()
piCam.preview_configuration.main.size=(dispW, dispH)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.transform=Transform(vflip=1, hflip=1)
piCam.preview_configuration.controls.FrameRate=30
piCam.preview_configuration.align()
piCam.configure("preview")

encoder = H264Encoder(1000000)
# print(videoNameAndFormat)
encoder.output = FfmpegOutput(videoNameAndFormat)
piCam.start()

while True:
    frame = piCam.capture_array()
    cv2.imshow("Camera", frame)
    
    if cv2.waitKey(1) == ord('a'):
        print('Button a pressed')
        piCam.start_encoder(encoder)
    
    if cv2.waitKey(1) == ord('b'):
        print('Button b pressed')
        piCam.stop_encoder()
    
    if cv2.waitKey(1) == ord('q'):
        print('Button q pressed') 
        break

piCam.stop()
cv2.destroyAllWindows()
