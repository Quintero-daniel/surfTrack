import cv2
import time

from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration())

encoder = H264Encoder(1000000)
encoder.output = FfmpegOutput('test.mp4')

# picam2.start_preview(Preview.QTGL)
picam2.start_encoder(encoder)
picam2.start()

time.sleep(2)
# while True:
#     
#     if cv2.waitKey(1) == ord('q'):
#         break

picam2.stop_encoder()
picam2.stop()

