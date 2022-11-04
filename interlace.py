import cv2 
import numpy as np
# Paths to the 2 images
IMAGE1_PATH = "./images/dog3.jpeg"
IMAGE2_PATH = "./images/dog4.jpeg"

N_IMAGES = 2
LPI = 60 # Lenticules per inch; requires pitch test
PRP = 120 # dpi; dots per inch; Resolution of your inkjet or color laser printer

TARGET_H_INCH = 3 #inches
TARGET_B_INCH = 4 #inches
TARGET_H = TARGET_H_INCH*PRP
TARGET_B = TARGET_B_INCH*PRP


def assertImageShape(image):
    imageH,imageB,imageC = image.shape[0],image.shape[1],image.shape[2]
    assert imageC == 3, "Input image should has 3 channels"
    assert (imageH/TARGET_H) == (imageB/TARGET_B), f"Input image should has the ratio {TARGET_H}:{TARGET_B}"

def reshapeImage(image):
    imageH,imageB,imageC = image.shape[0],image.shape[1],image.shape[2]
    assert imageC == 3, "Input image should has 3 channels"
    if imageH != TARGET_H or imageB != TARGET_B:
        print(f"the original shape of the image: {imageH}, {imageB}, {imageC}")
        resizedImage = cv2.resize(image,(TARGET_H,TARGET_B,3),interpolation = cv2.INTER_AREA)
        h,b,c = resizedImage.shape
        print(f"reshaping to: {h}, {b}, {c}")
        return resizedImage
    return image


image1 = reshapeImage(cv2.imread(IMAGE1_PATH))
image2 = reshapeImage(cv2.imread(IMAGE2_PATH))


    

cv2.imshow("image", image_out)
cv2.waitKey()





