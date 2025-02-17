import tkinter as tk
import cv2

from tkinter import *
from PIL import Image, ImageTk


class WebcampApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Webcam App")
        
        self.current_image = Image.open('/home/dan/Downloads/surf.jpeg').resize((380, 200))
        self.photo = ImageTk.PhotoImage(image=self.current_image)
        self.label_for_color_image = Label(self.window)
        self.label_for_mask_image = Label(self.window)
        
        self.color_image_checkbutton_var = IntVar()
        Checkbutton(window, variable=self.color_image_checkbutton_var, onvalue=1, offvalue=0).place(x=230, y=215)
        
        self.mask_image_checkbutton_var = IntVar()
        Checkbutton(window, variable=self.mask_image_checkbutton_var, onvalue=1, offvalue=0).place(x=230, y=445)
        
        self.refresh_images()

        
    def refresh_images(self):
        self.check_buttons_pressed()
        self.window.after(5000, self.refresh_images)
        
    def check_buttons_pressed(self):
        if not self.color_image_checkbutton_var.get():
            self.label_for_color_image.configure(image=self.photo)
            self.label_for_color_image.place(x=10, y=10)
        else:
            self.label_for_color_image.place_forget()
            
        if not self.mask_image_checkbutton_var.get():
            self.label_for_mask_image.configure(image=self.photo)
            self.label_for_mask_image.place(x=420, y=10)
        else:
            self.label_for_mask_image.place_forget()
            
        
# Size of the Window = 800x410
if __name__== '__main__':
    root = tk.Tk()
    # Window sometimes doesn't spawn zoomed therefore we make sure it
    # does after 200ms
    root.after(200, lambda: root.attributes('-zoomed', True))
    app = WebcampApp(root)
    root.mainloop()    

