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

	# The lines below are for saving the image
	name = str(datetime.now()).replace(" ", "_")
	im.save("./interlaced/"+name+".jpeg",dpi=(NUM*LPI, NUM*60))
	print("outputted")


import sys 
print("input image file path")
for line in sys.stdin:
	tokens = line.rstrip().split()
	if len(tokens) != 2:
		print("error: incorrect number of input tokens")
	else:
		interlace(tokens[0],tokens[1])
 
print("Exit")
