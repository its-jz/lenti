import sys, time
import RPi.GPIO as GPIO
import cv2
from PIL import Image
import numpy as np
from datetime import datetime

red,green,blue = 11,13,15
button = 16

c1 = cv2.VideoCapture(0)
c2 = cv2.VideoCapture(2)

GPIO.setwarnings(False)

def blink(pin):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)

def turnOff(pin):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)	
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN)
def takePic():
	print("taking pictures")
	ret,img1= c1.read()
	ret,img2= c2.read()
	return img1,img2

def toWritableImage(img):
	image = np.array(img)
	image.setflags(write=1)
	return np.transpose(image,(1,0,2))
	
def interlace(img1,img2):
	img1,img2 = Image.fromarray(img1),Image.fromarray(img2)
	
	LPI = 60
	w_inch = 4
	h_inch = 3
	NUM= 2
	img_w,img_h = int(LPI*w_inch*NUM),60*h_inch*NUM
	
	print("interlacing")
	
	image1 = toWritableImage(img1)
	image2 = toWritableImage(img2)
	
	h1,w1,c1 = image1.shape
	h2,w2,c2 = image2.shape

	for i in range(h1):
		if i%2 == 1:
			image1[i,:,:] = 0

	for i in range(h2):
		if i%2 == 0:
			image2[i,:,:] =0

	output = image1 + image2
	
	

	
	im = Image.fromarray(output)

	return output

from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox

root = Tk()
root.minsize(800, 480)
root.maxsize(800, 480)

preview = ttk.Frame(root)
preview.pack()
def printBtn():
	messagebox.showinfo( "Print", "Print Picture")
def retakeBtn():
	messagebox.showinfo( "Retake", "Retake Picture")
printBtn = Button(preview, text ="Print", command = printBtn)
printBtn.pack()
retakeBtn = Button(preview, text ="Retake", command = retakeBtn)
retakeBtn.pack()
def show_camera_preview():
	ret1, frame1 = c1.read()
	ret2, frame2 = c2.read()
	frame1 = cv2.flip(frame1, 1)
	frame2 = cv2.flip(frame2, 1)
	frame = interlace(frame1,frame2)
	rotatedframe = np.rot90(frame, k=1, axes=(1,0))
	
	cv2image = cv2.cvtColor(rotatedframe, cv2.COLOR_BGR2RGBA)
	img = Image.fromarray(cv2image)
	imgtk = ImageTk.PhotoImage(image=img)
	preview.imgtk = imgtk
	preview.configure(image=imgtk)
	preview.after(10, show_frame)
	if (GPIO.input(button) == 0):
		tempName = str(datetime.now()).replace(" ","_")
		filePath = "./previews/"+tempName+".jpeg"
		cv2.imwrite(filePath,rotatedframe)
		img = ImageTk.PhotoImage(Image.open(filePath))
		# Create a Label Widget to display the text or Image
		preview.imgtk = img
		preview.configure(image=img)
		preview.after(10, show_frame)
show_camera_preview()

root.mainloop()
 
