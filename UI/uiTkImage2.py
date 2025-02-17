import tkinter as tk
import cv2

from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from picamera2 import Picamera2, Preview
from libcamera import Transform

buttonState = False

class WebcampApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Webcam App")
        self.entry = tk.Entry(window)
        stvar=tk.StringVar()
        stvar.set("one")

        self.canvas=tk.Canvas(window, width=200, height=200, background='white')
        self.canvas.grid(row=0,column=1)

        frame = Frame(self.window, height=200, width=200)
        frame.grid(row=0,column=0, sticky="n")

        self.option=tk.OptionMenu(frame, stvar, "one", "two", "three")
        label1=Label(frame, text="Figure").grid(row=0,column=0, sticky="nw")
        label2=Label(frame, text="X").grid(row=1,column=0, sticky="w")
        label3=Label(frame, text="Y").grid(row=2,column=0, sticky="w")
        self.option.grid(row=0,column=1,sticky="nwe")
        entry = Entry(frame).grid(row = 1,column = 1,sticky = E+ W)
        entry1 = Entry(frame).grid(row = 2,column = 1, sticky = E)
        Button1=Button(frame,text="Draw").grid(row = 3,column = 1, sticky = "we")
        figure1=self.canvas.create_rectangle(80, 80, 120, 120, fill="blue")
        
#         self.update_cam_image()
        
    def update_cam_image(self):
        self.current_image = Image.open('/home/dan/Downloads/surf.jpeg')
        self.photo = ImageTk.PhotoImage(image=self.current_image)
        self.canvas.create_image(0,0,image=self.photo, anchor=tk.NW)


if __name__== '__main__':
    root = tk.Tk()
    root.maxsize(800, 420)
    root.minsize(800, 420)
    app = WebcampApp(root)
    root.mainloop()    

