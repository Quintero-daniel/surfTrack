import tkinter as tk
import cv2
import numpy as np
import time
import pantilthat

from fps import Fps
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from picamera2 import Picamera2, Preview
from libcamera import Transform
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput


class WebcampApp:
    def __init__(self, window):
        self.display_w, self.display_h = 385, 200
        self.window = window
        self.window.title("Webcam App")
        self.default_color = window.cget("bg")
        self.configure_camera(self.display_w, self.display_h)
        self.fps = Fps()

        self.panError = 0
        self.tiltError = 0
        self.panAngle = 0
        self.tiltAngle = 0
        pantilthat.pan(self.panAngle)
        pantilthat.tilt(self.tiltAngle)

        self.color_image_label = Label(self.window)
        self.mask_image_label = Label(self.window)
        
        self.color_image_checkbutton_var = IntVar()
        Checkbutton(window, variable=self.color_image_checkbutton_var, onvalue=1, offvalue=0).place(x=200, y=220)
        
        self.mask_image_checkbutton_var = IntVar()
        Checkbutton(window, variable=self.mask_image_checkbutton_var, onvalue=1, offvalue=0).place(x=600, y=220)

        self.scale_one_var = IntVar()
        self.scale_one = Scale(window, variable=self.scale_one_var, width=10, borderwidth=0, length=385, from_=0, to=255, tickinterval=0, orient=HORIZONTAL)
        self.scale_one.place(x=10, y=225)

        self.scale_two_var = IntVar()
        self.scale_two = Scale(window, variable=self.scale_two_var, width=10, borderwidth=0, length=385, from_=0, to=255, tickinterval=0, orient=HORIZONTAL)
        self.scale_two.place(x=10, y=260)

        self.scale_three_var = IntVar()
        self.scale_three = Scale(window, variable=self.scale_three_var, width=10, borderwidth=0, length=385, from_=0, to=255, tickinterval=0, orient=HORIZONTAL)
        self.scale_three.place(x=10, y=295)

        self.scale_four_var = IntVar()
        self.scale_four = Scale(window, variable=self.scale_four_var, width=10, borderwidth=0, length=385, from_=0, to=255, tickinterval=0, orient=HORIZONTAL)
        self.scale_four.place(x=405, y=225)

        self.scale_five_var = IntVar()
        self.scale_five = Scale(window, variable=self.scale_five_var, width=10, borderwidth=0, length=385, from_=0, to=255, tickinterval=0, orient=HORIZONTAL)
        self.scale_five.place(x=405, y=260)

        self.scale_six_var = IntVar()
        self.scale_six = Scale(window, variable=self.scale_six_var, width=10, borderwidth=0, length=385, from_=0, to=255, tickinterval=0, orient=HORIZONTAL)
        self.scale_six.place(x=405, y=295)
        
        self.rec_button_state = False
        self.rec_button = Button(text ="REC", fg='red', bg=self.default_color, command=self.rec_command)
        self.rec_button.place(x=740, y=380)
        self.track_button_state = False
        self.track_button = Button(text ="Track", fg='red', bg=self.default_color, command=self.track_command)
        self.track_button.place(x=680, y=380) 
        self.refresh_images()

    def refresh_images(self):
        time_start = time.time()
        frame = self.piCam.capture_array()
        frame, mask = self.calculate_frames(frame)

        current_color_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        current_mask_image = Image.fromarray(cv2.cvtColor(mask, cv2.COLOR_BGR2RGB))
        self.color_photo = ImageTk.PhotoImage(image=current_color_image)
        self.mask_photo = ImageTk.PhotoImage(image=current_mask_image)

        self.check_buttons_pressed()
        time_end = time.time()
        loop_time = time_end - time_start
        self.fps.fps_counter = .9 * self.fps.fps_counter + .1 * (1 / loop_time)
        self.window.after(15, self.refresh_images)

    def calculate_frames(self, frame):
        lowerBound = np.array([self.scale_one_var.get(), self.scale_two_var.get(), self.scale_three_var.get()])
        upperBound = np.array([self.scale_four_var.get(), self.scale_five_var.get(), self.scale_six_var.get()])

        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
        objectOfInterest = cv2.bitwise_and(frame, frame, mask=myMask)
        contours, junk = cv2.findContours(myMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if self.track_button_state:
            if len(contours) > 0:
                contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
                # cv2.drawContours(frame, contours,  0, (255, 0, 0), 3)
                contour = contours[0]
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

                panCalc = (x+w/2)-self.display_w/2
                if panCalc > self.panError + 5 or panCalc < self.panError - 5:
                    self.panError = panCalc
                    self.panAngle = self.panAngle - self.panError/75

                    if self.panAngle <-90:
                        self.panAngle=-90
                    if self.panAngle >90:
                        self.panAngle=90
                    if abs(self.panError) > 35:
                        pantilthat.pan(self.panAngle)

                tiltCalc = (y+h/2)-self.display_h/2
                if tiltCalc > self.tiltError + 5 or tiltCalc < self.tiltError - 5:
                    self.tiltError = tiltCalc
                    self.tiltAngle = self.tiltAngle + self.tiltError/75

                    if self.tiltAngle <-90:
                        self.tiltAngle=-90
                    if self.tiltAngle >40:
                        self.tiltAngle=40
                    if abs(self.tiltError) > 35:
                        pantilthat.tilt(self.tiltAngle)
            
        cv2.putText(frame, str(int(self.fps.fps_counter)) + " fps", self.fps.fps_text_position, self.fps.fps_text_font,
                    self.fps.fps_text_height, self.fps.fps_text_color, self.fps.fps_text_weight)

        return frame, myMask

    def check_buttons_pressed(self):
        if not self.color_image_checkbutton_var.get():
            self.color_image_label.configure(image=self.color_photo)
            self.color_image_label.place(x=10, y=10)
        else:
            self.color_image_label.place_forget()

        if not self.mask_image_checkbutton_var.get():
            self.mask_image_label.configure(image=self.mask_photo)
            self.mask_image_label.place(x=405, y=10)
        else:
            self.mask_image_label.place_forget()

    def rec_command(self):
        time_now = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")).replace(" ", "")
        video_name_and_format =  time_now + '.mp4'

        # Button pressed
        if self.rec_button_state is False:
            self.encoder.output = FfmpegOutput(video_name_and_format)
            self.piCam.start_encoder(self.encoder)
            self.rec_button_state = True
            self.rec_button.configure(relief='sunken', fg='white', bg='red')
            self.hide_widgets()
        # Button de-pressed
        else:
            self.piCam.stop_encoder()
            self.rec_button_state = False
            self.rec_button.configure(relief='raised', fg='red', bg=self.default_color)
            self.show_widgets()
            
    def track_command(self):
        # Button pressed
        if self.track_button_state is False:
            self.track_button_state = True
            self.track_button.configure(relief='sunken')
        # Button de-pressed
        else:
            self.track_button_state = False
            self.track_button.configure(relief='raised')
        
    def hide_widgets(self):
        self.scale_one.configure(state='disabled', fg='white')
        self.scale_two.configure(state='disabled', fg='white')
        self.scale_three.configure(state='disabled', fg='white')
        self.scale_four.configure(state='disabled', fg='white')
        self.scale_five.configure(state='disabled', fg='white')
        self.scale_six.configure(state='disabled', fg='white')
        
    def show_widgets(self):
        self.scale_one.configure(state='normal', fg='black')
        self.scale_two.configure(state='normal', fg='black')
        self.scale_three.configure(state='normal', fg='black')
        self.scale_four.configure(state='normal', fg='black')
        self.scale_five.configure(state='normal', fg='black')
        self.scale_six.configure(state='normal', fg='black')
        
    def configure_camera(self, display_w, display_h):
        self.piCam = Picamera2()
        self.piCam.preview_configuration.main.size=(display_w, display_h)
        self.piCam.preview_configuration.main.format="RGB888"
        self.piCam.preview_configuration.transform=Transform(vflip=1, hflip=1)
        self.piCam.preview_configuration.controls.FrameRate=30
        self.piCam.preview_configuration.align()
        self.piCam.configure("preview")
        self.encoder = H264Encoder(1000000)
        self.piCam.start()
                
# Size of the Window = 800x410
if __name__== '__main__':
    root = tk.Tk()
    # Window sometimes doesn't spawn zoomed therefore we make sure it
    # does after 200ms
    root.after(200, lambda: root.attributes('-zoomed', True))
    app = WebcampApp(root)
    root.mainloop()


