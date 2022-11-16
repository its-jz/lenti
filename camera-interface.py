import tkinter as tk                # python 3
from tkinter import font as tkfont


import sys, time
import RPi.GPIO as GPIO
import cv2
from PIL import Image,ImageTk
import numpy as np
from datetime import datetime

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (ViewFinderPage, PreviewPage, PrintPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ViewFinderPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class ViewFinderPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # label = tk.Label(self, text="ViewFinder", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)

        # lbl_webcam_display = tk.Label(label)
        # lbl_webcam_display.grid(row=0,column=0)
        # c1 = cv2.VideoCapture(0)
        # c2 = cv2.VideoCapture(2)
        # ret1, pic1 = c1.read()
        # # ret2, pic2= c2.read()

        # def display_webcam():
        #     cv2image= cv2.cvtColor(pic1,cv2.COLOR_BGR2RGB)
        #     img = Image.fromarray(cv2image)
        #     imgtk = ImageTk.PhotoImage(image = img)
        #     lbl_webcam_display.imgtk = imgtk
        #     lbl_webcam_display.configure(image=imgtk)
        #     lbl_webcam_display.after(20,display_webcam)
        # display_webcam()
        # Create a Label to capture the Video frames
        label =tk.Label(self)
        label.pack()
        cap= cv2.VideoCapture(0)

        # Define function to show frame
        def show_frames():
        # Get the latest frame and convert into Image
            cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            # Convert image to PhotoImage
            imgtk = ImageTk.PhotoImage(image = img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
            # Repeat after an interval to capture continiously
            label.after(20, show_frames)
        show_frames()  


        button = tk.Button(self, text="Placeholder for taking an Image ",
                    command=lambda: controller.show_frame("PreviewPage"))
        button.pack()
class PreviewPage(tk.Frame):

    def __init__(self, parent, controller):
        def onClickPrint():
            controller.show_frame("PrintPage")
        def onClickRetake():
            controller.show_frame("ViewFinderPage")

        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Preview Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


        btn_print = tk.Button(self, text="Print",
                            command=onClickPrint)
        btn_retake = tk.Button(self, text="Retake",
                            command=onClickRetake)
        btn_print.pack()
        btn_retake.pack()

class PrintPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Printing, please wait", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Take Another Picture",
                           command=lambda: controller.show_frame("ViewFinderPage"))
        button.pack()



    






if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()