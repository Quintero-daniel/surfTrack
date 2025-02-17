import cv2
import time
from picamera2 import Picamera2

piCam = Picamera2()
piCam.preview_configuration.main.size=(640, 360)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.controls.FrameRate=30
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

fps = 0
fps_text_position = (10,30)
fps_text_font = cv2.FONT_HERSHEY_SIMPLEX
fps_text_height = 0.5
fps_text_color = (0,0,255)
fps_text_weight = 1

while True:
    time_start = time.time()
    frame = piCam.capture_array()
    cv2.putText(frame, str(int(fps)), fps_text_position, fps_text_font, fps_text_height, fps_text_color, fps_text_weight)
    cv2.imshow("piCam", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break
    
    time_end = time.time()
    loop_time = time_end - time_start
    fps = .9*fps + .1*(1/loop_time)
    print(int(fps))

cv2.destroyAllWindows()
