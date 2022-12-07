from datetime import datetime
import sys, time
import cv2
from PIL import Image
import numpy as np
from datetime import datetime

def toWritableImage(img):
	image = np.array(img)
	image.setflags(write=1)
	return np.transpose(image,(1,0,2))


def interlace(img1,img2):
	img1,img2 = Image.fromarray(img1),Image.fromarray(img2)
	
	LPI = 60
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
	#name = str(datetime.now()).replace(" ", "_")
	name = "40lpi"
	im.save("./output/"+name+".jpeg",dpi=(NUM*LPI, NUM*LPI))
	#im.save("./output/"+name+".jpeg",dpi=(120.2, 120.2))

	print("outputted")



dim = (160, 240)
#dim = (750, 500)


img1 = cv2.imread("./images/dog3.jpeg", 1)
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB) #convert it into RGB format
img1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
img2 = cv2.imread("./images/dog4.jpeg", 1)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB) #convert it into RGB format
img2 = cv2.resize(img2, dim, interpolation = cv2.INTER_AREA)

interlace(img1,img2)