import tkinter as tk                # python 3
from tkinter import font as tkfont
import os


import pathlib
import pandas as pd
import dropbox
from dropbox.exceptions import AuthError

from datetime import datetime
import sys, time
import cv2
from PIL import Image
import numpy as np
from datetime import datetime

import sys, time
import RPi.GPIO as GPIO
import cv2
from PIL import Image,ImageTk
import numpy as np
from datetime import datetime
c1 = cv2.VideoCapture(0)
c2 = cv2.VideoCapture(2)
DROPBOX_ACCESS_TOKEN = "sl.BUjJfk96_y4d5qGb9eMJNtemOgefQnw8J6uAd2sEEE9AEscMa6Za1nQ0X6GZ66KdboX3oltH74OdIwo6Junt_IhBRTQCOP1Q2ECJSyW_2zdDjYNGR_ClLY5oCiCNbw9Xmmazxpkzb1k3"


class SampleApp(tk.Tk):

   def __init__(self, *args, **kwargs):
      # if(os.path.exists('./preview.jpeg')):
      #    print("file exists")
      #    os.remove('./preview.jpeg')
      # else:
      #    print("clean no preview")



      tk.Tk.__init__(self, *args, **kwargs)
      self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

      # the container is where we'll stack a bunch of frames
      # on top of each other, then the one we want visible
      # will be raised above the others
      container = tk.Frame(self)
      container.pack(side="top", fill="both", expand=True)
      container.grid_rowconfigure(0, weight=1)
      container.grid_columnconfigure(0, weight=1)
      self.container = container
      viewFinderFrame = ViewFinderPage(parent=container, controller=self)
      viewFinderFrame.grid(row=0, column=0, sticky="nsew")
      self.viewFinderFrame = viewFinderFrame

   def show_frame(self, page_name, img1=None, img2 = None):
      '''Show a frame for the given page name'''
      container = self.container
      
      
      if page_name == "ViewFinderPage":
         self.viewFinderFrame.destroy()
         viewFinderFrame = ViewFinderPage(parent=container, controller=self)
         viewFinderFrame.grid(row=0, column=0, sticky="nsew")
         self.viewFinderFrame = viewFinderFrame
         viewFinderFrame.tkraise()
      elif page_name == "PreviewPage":
         previewPageFrame = PreviewPage(parent=container, controller=self, img1 = img1, img2 = img2)
         previewPageFrame.grid(row=0, column=0, sticky="nsew")
         previewPageFrame.tkraise()
      else:
         printPageFrame = PrintPage(parent=container, controller=self,img1 = img1, img2 = img2)
         printPageFrame.grid(row=0, column=0, sticky="nsew")
         printPageFrame.tkraise()

class ViewFinderPage(tk.Frame):
   def __init__(self, parent, controller):
      tk.Frame.__init__(self, parent)
      self.controller = controller
      label =tk.Label(self)
      label.pack()
      self.running = True
      # Define function to show frame
      def show_frames():
      # Get the latest frame and convert into Image
         cv2image= cv2.cvtColor(c1.read()[1],cv2.COLOR_BGR2RGB)
         img = Image.fromarray(cv2image)
         # Convert image to PhotoImage
         imgtk = ImageTk.PhotoImage(image = img)
         label.imgtk = imgtk
         label.configure(image=imgtk)
         # Repeat after an interval to capture continiously
         if self.running == True:
            label.after(20, show_frames)
         else:
            print("not running")
      show_frames()

      def takePic():
         self.running = False
         ret1,img1 = c1.read()
         ret2,img2 = c2.read()
         img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
         img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
         controller.show_frame("PreviewPage",img1=img1,img2=img2)
         return
      
      button = tk.Button(self, text="Placeholder for taking an Image ",
                  command=lambda: takePic())
      button.pack()




class PreviewPage(tk.Frame):

    def __init__(self, parent, controller, img1 = None, img2 = None):
      def onClickPrint():
         controller.show_frame("PrintPage",img1=img1,img2=img2)
      def onClickRetake():
         controller.show_frame("ViewFinderPage")
      image = img1
      tk.Frame.__init__(self, parent)
      self.controller = controller
      # label = tk.Label(self, text="Preview Page", font=controller.title_font)
      # label.pack(side="top", fill="x", pady=10)
      image = Image.fromarray(image)
      img = ImageTk.PhotoImage(image)
      imgLabel = tk.Label(self,image=img)
      imgLabel.image = img
      imgLabel.pack()
      btn_container = tk.Label(self)
      btn_print = tk.Button(btn_container, text="Print",
                           command=onClickPrint)
      btn_retake = tk.Button(btn_container, text="Retake",
                           command=onClickRetake)
      btn_print.grid(row=0, column=0, sticky="nsew")
      btn_retake.grid(row=0, column=1, sticky="nsew")
      btn_container.pack()


class PrintPage(tk.Frame):





   def __init__(self, parent, controller, img1 = None, img2 = None):
      def dropbox_connect():
         try:
            dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
         except AuthError as e:
            print('Error connecting to Dropbox with access token: ' + str(e))
         return dbx
      
      def upload(name):
         try:
            dbx = dropbox_connect()
            f=open("./output/"+name+".jpeg","rb")
            meta = dbx.files_upload(f.read(), "/lenti/"+name+".jpeg")
         except AuthError as e:
            print('Error uploading to Dropbox with access token: ' + str(e))


      def toWritableImage(img):
	      image = np.array(img)
	      image.setflags(write=1)
	      return np.transpose(image,(1,0,2))


      def interlace(img1,img2):
         print("here1")
         img1,img2 = Image.fromarray(img1),Image.fromarray(img2)
      
         LPI = 40
         #w_inch = 2
         #h_inch = 3
         NUM = 2
         #img_w,img_h = int(LPI*w_inch*NUM),60*h_inch*NUM
         
         print("interlacing")
         
         image1 = toWritableImage(img1)
         image2 = toWritableImage(img2)
         h1,w1,c1 = image1.shape
         h2,w2,c2 = image2.shape

         count = 0 
         for i in range(h1):
            if i%2 == 1:
               image1[i,:,:] = 0
               count +=1

         for i in range(h2):
            if i%2 == 0:
               image2[i,:,:] =0

         output = image1 + image2
               
         print(output.shape)


         
         im = Image.fromarray(output)

         # The lines below are for saving the image
         name = str(datetime.now()).replace(" ", "_")
         im.save("./output/"+name+".jpeg",dpi=(NUM*LPI, NUM*LPI))

         return name

      print(f'img1: {img1.shape}')
      print(f'img2: {img2.shape}')
      print(type(img1))
      print(type(img2))
      name = interlace(img1=img1,img2=img2)
      upload(name)

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

