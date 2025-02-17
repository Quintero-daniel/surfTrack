# digamos que 28m es la maxima distancia de zoom
# 7 metros es la maxima distancia que es capaz de ver la pelota

import cv2
import time

from picamera2 import Picamera2, Preview
from libcamera import Transform

# Global vars
dispW = 640
dispH = 360

fps = 0
fps_text_position = (10,30)
fps_text_font = cv2.FONT_HERSHEY_SIMPLEX
fps_text_height = 0.5
fps_text_color = (0,0,255)
fps_text_weight = 1

piCam = Picamera2()
piCam.preview_configuration.main.size=(dispW, dispH)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.controls.FrameRate=30
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

size = piCam.capture_metadata()['ScalerCrop'][2:]
full_res = piCam.camera_properties['PixelArraySize']
offset = [(r - s) // 2 for r, s in zip(full_res, size)]

while True:
    piCam.capture_metadata()
    time_start = time.time()
    frame = piCam.capture_array()
    
    cv2.putText(frame, str(int(fps)), fps_text_position, fps_text_font, fps_text_height, fps_text_color, fps_text_weight)
    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break
    if cv2.waitKey(1) == ord('a'):
        # Zoom in
        size = [int(s * 0.95) for s in size]
        offset = [(r - s) // 2 for r, s in zip(full_res, size)]
        # Lock in the maximum
        piCam.set_controls({"ScalerCrop": offset + size})
    if cv2.waitKey(1) == ord('s'):
        # Zoom out
        size = [int(s + (s * 0.05)) for s in size]
        offset = [(r - s) // 2 for r, s in zip(full_res, size)]
        piCam.set_controls({"ScalerCrop": offset + size})

    print("size: " + str(size) + " offset: " + str(offset))

    time_end = time.time()
    loop_time = time_end - time_start
    fps = .9*fps + .1*(1/loop_time)

cv2.destroyAllWindows()