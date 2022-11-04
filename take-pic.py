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
	img1,img2= cv2.cvtColor(img1,cv2.COLOR_BGR2RGB),cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
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
	
	name = str(datetime.now()).replace(" ", "_")

	
	im = Image.fromarray(output)
	im.save("./output/"+name+".jpeg",dpi=(NUM*LPI, NUM*60))
	print("outputted")
	
	

while True:
	if(GPIO.input(button) == 0):
		blink(red)
		img1,img2 = takePic()
		interlace(img1,img2)
	else:
		turnOff(red)
