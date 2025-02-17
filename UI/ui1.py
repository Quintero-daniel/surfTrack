import cv2 as cv; cv2=cv
import numpy as np

from picamera2 import Preview

root_wind = 'main';

cv.namedWindow(root_wind,cv.WINDOW_AUTOSIZE)


def on_hello(*args):
    print('hello', args)

cv.createButton('hello', on_hello, None, cv.QT_PUSH_BUTTON)

img = np.ones((480, 640), np.uint8)
# img.fill(127)

while True:
    
    cv.imshow(root_wind, img)
    
    code = cv.waitKey(1)
    
    if code == ord('q'):
        break
    
cv.destroyAllWindows()
