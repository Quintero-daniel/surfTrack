import tkinter as tk
import cv2
import numpy as np

from tkinter import *
from PIL import Image, ImageTk

from PIL import Image, ImageTk
from datetime import datetime
from picamera2 import Picamera2, Preview
from libcamera import Transform


class WebcampApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Webcam App")
        self.default_color = window.cget("bg")
        self.configure_camera()

        self.color_image_label = Label(self.window)
        self.mask_image_label = Label(self.window)
        
        self.color_image_checkbutton_var = IntVar()
        Checkbutton(window, variable=self.color_image_checkbutton_var, onvalue=1, offvalue=0).place(x=200, y=220)
        
        self.mask_image_checkbutton_var = IntVar()
        Checkbutton(window, variable=self.mask_image_checkbutton_var, onvalue=1, offvalue=0).place(x=600, y=220)

        # state=tk.DISABLED
        self.scale_one = Scale(window, width=10, borderwidth=0, length=385, from_=0, to=255, tickinterval=0, orient=HORIZONTAL)
        self.scale_one.place(x=10, y=225)
        
        self.scale_two = Scale(window, width=10, borderwidth=0, length=385, from_=0, to=255, tickinterval=0, orient=HORIZONTAL)
        self.scale_two.place(x=10, y=260)
        
        self.scale_three = Scale(window, width=10, borderwidth=0, length=385, from_=0, to=255, tickinterval=0, orient=HORIZONTAL)
        self.scale_three.place(x=10, y=295)
        
        self.scale_four = Scale(window, width=10, borderwidth=0, length=385, from_=0, to=255, tickinterval=0, orient=HORIZONTAL)
        self.scale_four.place(x=405, y=225)
        
        self.scale_five = Scale(window, width=10, borderwidth=0, length=385, from_=0, to=255, tickinterval=0, orient=HORIZONTAL)
        self.scale_five.place(x=405, y=260)
        
        self.scale_six = Scale(window, width=10, borderwidth=0, length=385, from_=0, to=255, tickinterval=0, orient=HORIZONTAL)
        self.scale_six.place(x=405, y=295)
        
        self.rec_button_state = False
        self.rec_button = Button(text ="REC", fg='red', bg=self.default_color, command=self.rec_command)
        self.rec_button.place(x=740, y=380)       
        self.refresh_images()

        
    def refresh_images(self):
        current_image = Image.fromarray(cv2.cvtColor(self.piCam.capture_array(), cv2.COLOR_BGR2RGB))
        self.photo = ImageTk.PhotoImage(image=current_image)
        
        self.check_buttons_pressed()
        self.window.after(15, self.refresh_images)
        
    def check_buttons_pressed(self):
        if not self.color_image_checkbutton_var.get():
            self.color_image_label.configure(image=self.photo)
            self.color_image_label.place(x=10, y=10)
        else:
            self.color_image_label.place_forget()
            
        if not self.mask_image_checkbutton_var.get():
            self.mask_image_label.configure(image=self.photo)
            self.mask_image_label.place(x=405, y=10)
        else:
            self.mask_image_label.place_forget()

    def rec_command(self):
        if self.rec_button_state is False:
            self.rec_button_state = True
            self.rec_button.configure(relief='sunken', fg='white', bg='red')
            self.hide_wiggets()
        else:
            self.rec_button_state = False
            self.rec_button.configure(relief='raised', fg='red', bg=self.default_color)
            self.show_wiggets()
        
    def hide_wiggets(self):
        self.scale_one.configure(state='disabled', fg='white')
        self.scale_two.configure(state='disabled', fg='white')
        self.scale_three.configure(state='disabled', fg='white')
        self.scale_four.configure(state='disabled', fg='white')
        self.scale_five.configure(state='disabled', fg='white')
        self.scale_six.configure(state='disabled', fg='white')
        
    def show_wiggets(self):
        self.scale_one.configure(state='normal', fg='black')
        self.scale_two.configure(state='normal', fg='black')
        self.scale_three.configure(state='normal', fg='black')
        self.scale_four.configure(state='normal', fg='black')
        self.scale_five.configure(state='normal', fg='black')
        self.scale_six.configure(state='normal', fg='black')
        
    def configure_camera(self):
        self.piCam = Picamera2()
        self.piCam.preview_configuration.main.size=(385, 200)
        self.piCam.preview_configuration.main.format="RGB888"
        self.piCam.preview_configuration.transform=Transform(vflip=1, hflip=1)
        self.piCam.preview_configuration.controls.FrameRate=30
        self.piCam.preview_configuration.align()
        self.piCam.configure("preview")
        self.piCam.start()
                
# Size of the Window = 800x410
if __name__== '__main__':
    root = tk.Tk()
    # Window sometimes doesn't spawn zoomed therefore we make sure it
    # does after 200ms
    root.after(200, lambda: root.attributes('-zoomed', True))
    app = WebcampApp(root)
    root.mainloop()


