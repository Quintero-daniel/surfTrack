import tkinter as tk
import cv2

from PIL import Image, ImageTk
from datetime import datetime
from picamera2 import Picamera2, Preview
from libcamera import Transform

buttonState = False

class WebcampApp:
    def __init__(self, window):
        
        self.window = window
        self.window.title("Webcam App")
        
        self.canvas = tk.Canvas(window, width=800, height=380)
        self.canvas.pack()
        
        self.button = tk.Button(window, text="ButtonTest", command=self.button_action)
        self.button.pack()
        
        self.update_cam_image()
        
    def update_cam_image(self):
        self.current_image = Image.open('/home/dan/Downloads/surf.jpeg')
        self.photo = ImageTk.PhotoImage(image=self.current_image)
        self.canvas.create_image(0,0,image=self.photo, anchor=tk.NW)
        
    def button_action(self):
        global buttonState
        
        if buttonState is False:
            buttonState = True
        else:
            buttonState = False

root = tk.Tk()
app = WebcampApp(root)
root.mainloop()
