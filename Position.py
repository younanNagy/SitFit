import numpy as np
import cv2

class Position:

    def __init__(self):
        self.contour=None
        self.area=None
        self.image=None
        self.center=None

    def set_position(self,image,threshold):
        # get the contour of this position
        self.image=image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh_img = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY_INV)
        contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
        self.contour= max(contours, key = cv2.contourArea)
        center=cv2.moments(self.contour)
        self.center=(int(center["m10"] / center["m00"]), int(center["m01"] / center["m00"]))


    def get_difference(self):
        pass


    def get_correlation(self):
        pass


    def Compare(self):
        pass

position=Position()
position.SetPosition(2,4)
print(position.area,"   ",type(position.area))