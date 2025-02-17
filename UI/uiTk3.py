import tkinter as tk
import cv2
import time
import pantilthat
import numpy as np

from PIL import Image, ImageTk
from datetime import datetime
from picamera2 import Picamera2, Preview
from libcamera import Transform

buttonState = False
y = False

class WebcampApp:
    def __init__(self, window):
        
        self.window = window
        self.window.title("Webcam App")
        
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()
        
        self.button = tk.Button(window, text="ButtonTest", command=self.button_action)
        self.button.pack()
        
        self.configure_camera()
        self.update_cam_image()
        
    def update_cam_image(self):
        self.current_image = Image.fromarray(cv2.cvtColor(self.piCam.capture_array(), cv2.COLOR_BGR2RGB))
        self.photo = ImageTk.PhotoImage(image=self.current_image)
        self.photo1 = ImageTk.PhotoImage(image=self.current_image)
        self.canvas.create_image(0,0,image=self.photo, anchor=tk.NW)
        self.canvas.create_image(320,240,image=self.photo1, anchor=tk.NW)
        
#         if buttonState:
#             self.canvas.create_oval(20, 20, 5, 5, fill="red")
        
        self.window.after(15, self.update_cam_image)
        
    def button_action(self):
        global buttonState
        global y
        
        if buttonState is False:
            buttonState = True
        else:
            buttonState = False
        
    def configure_camera(self):
        self.piCam = Picamera2()
        self.piCam.preview_configuration.main.size=(320, 240)
        self.piCam.preview_configuration.main.format="RGB888"
        self.piCam.preview_configuration.transform=Transform(vflip=1, hflip=1)
        self.piCam.preview_configuration.controls.FrameRate=30
        self.piCam.preview_configuration.align()
        self.piCam.configure("preview")
        self.piCam.start()
        
root = tk.Tk()
app = WebcampApp(root)
root.mainloop()
