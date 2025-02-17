import tkinter as tk
import cv2
import time
import pantilthat
import numpy as np

from PIL import Image, ImageTk
from datetime import datetime
from picamera2 import Picamera2, Preview
from libcamera import Transform

# Camera Settings
piCam = Picamera2()
piCam.preview_configuration.main.size=(640, 480)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.transform=Transform(vflip=1, hflip=1)
piCam.preview_configuration.controls.FrameRate=30
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()


class WebcampApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Webcam App")
        
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()
        
        self.button = tk.Button(window, text="ButtonTest", command=self.button_action)
        self.button.pack()
        
        self.update_cam_image()
        
    def update_cam_image(self):
        self.current_image = Image.fromarray(cv2.cvtColor(piCam.capture_array(), cv2.COLOR_BGR2RGB))
        self.photo = ImageTk.PhotoImage(image=self.current_image)
        self.canvas.create_image(0,0,image=self.photo, anchor=tk.NW)
        self.window.after(15, self.update_cam_image)
        
    def button_action(self):
        print("Button Pressed")
        
root = tk.Tk()
app = WebcampApp(root)
root.mainloop()