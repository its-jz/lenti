import sys, time
import RPi.GPIO as GPIO
import cv2
from PIL import Image
import numpy as np
from datetime import datetime

from tkinter import *
from PIL import Image, ImageTk
import cv2

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
	
	# The lines below are for saving the image
	#name = str(datetime.now()).replace(" ", "_")
	#im.save("./output/"+name+".jpeg",dpi=(NUM*LPI, NUM*60))
	#print("outputted")

# 0: preview, 1:picTaken
# ~ view = 0
# ~ while True:
    # ~ # Display the interlaced image on the screen

    # ~ ret1, frame1 = c1.read()
    # ~ ret2, frame2 = c2.read()
    # ~ # Preview
    # ~ if view == 0:

        # ~ interlacedImg = interlace(frame1,frame2)
        # ~ cv2.imshow("view finder",interlacedImg)
        # ~ if cv2.waitKey(1) & 0xFF == ord('q'):
            # ~ break
        # ~ if (GPIO.input(button) == 0):
            # ~ print("down")
            # ~ cv2.destroyAllWindows()
            # ~ view = 1
    # ~ if view == 1:
	# ~ root=Tk()
	# ~ a = Label(root, text="Hello, world!")
	# ~ a.pack()
	# ~ root.mainloop()

        
# ~ c1.release()
# ~ c2.release()
# ~ cv2.destroyAllWindows()
    
from tkinter import messagebox
    
width, height = 800, 600

root = Tk()
lmain = Label(root)
lmain.pack()

def show_frame():
	ret1, frame1 = c1.read()
	ret2, frame2 = c2.read()
	frame1 = cv2.flip(frame1, 1)
	frame2 = cv2.flip(frame2, 1)
	frame = interlace(frame1,frame2)
	cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
	img = Image.fromarray(cv2image)
	imgtk = ImageTk.PhotoImage(image=img)
	lmain.imgtk = imgtk
	lmain.configure(image=imgtk)
	lmain.after(10, show_frame)
	if (GPIO.input(button) == 0):
		tempName = str(datetime.now()).replace(" ","_")
		filePath = "./previews/"+tempName
		toSave = Image.fromarray(frame)
		cv2.imwrite(filePath,toSave)
		img = ImageTk.PhotoImage(Image.open(filePath))
		# Create a Label Widget to display the text or Image
		lmain.imgtk = img
		lmain.configure(image=img)
		lmain.after(10, show_frame)
def helloCallBack():
	messagebox.showinfo( "Hello Python", "Hello World")

printBtn = Button(root, text ="Print", command = helloCallBack)
printBtn.pack()
retakeBtn = Button(root, text ="Retake", command = helloCallBack)
retakeBtn.pack()


show_frame()
root.mainloop()
