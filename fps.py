import cv2


class Fps:
    def __init__(self):
        self.fps_counter = 0
        self.fps_text_position = (10, 15)
        self.fps_text_font = cv2.FONT_HERSHEY_SIMPLEX
        self.fps_text_height = 0.5
        self.fps_text_color = (0, 0, 255)
        self.fps_text_weight = 1
