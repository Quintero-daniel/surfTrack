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
piCam.preview_configuration.main.size=(320, 240)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.transform=Transform(vflip=1, hflip=1)
piCam.preview_configuration.controls.FrameRate=30
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

root = tk.Tk()
root.geometry("640x480")

root.label1 = tk.Label()

root.button = tk.Button()


root.label1.grid(row=0, column=0)
root.button.grid(row=0, column=1)



class WebcampApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Webcam App")
        
        root.button.config(window, text="ButtonTest", command=self.button_action)
        
        self.update_cam_image()
        
    def update_cam_image(self):
        self.current_image = Image.fromarray(cv2.cvtColor(piCam.capture_array(), cv2.COLOR_BGR2RGB))
        self.photo = ImageTk.PhotoImage(image=self.current_image)
        root.label(image=self.photo)

        self.window.after(15, self.update_cam_image)
        
    def button_action(self):
        print("Button Pressed")
        
app = WebcampApp(root)
root.mainloop()
