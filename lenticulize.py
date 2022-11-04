from PIL import Image
import numpy as np

LPI = 60.5
w_inch = 4
h_inch = 3
NUM= 2

img_w,img_h = int(LPI*w_inch*NUM),60*h_inch*NUM
print(img_w,img_h)
image1 = Image.open('./images/dog3.jpeg').resize((960,720))
image1 = np.array(image1)
image1.setflags(write=1)
print(image1.shape)
image1 = np.transpose(image1,(1,0,2))
print(image1.shape)

image2 = Image.open('./images/dog4.jpeg').resize((960,720))
image2 = np.array(image2)
image2.setflags(write=1)
image2 = np.transpose(image2,(1,0,2))


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
im.save("./output/image595.jpeg",dpi=(NUM*LPI, NUM*60))

