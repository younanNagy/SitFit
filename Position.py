import numpy as np
import cv2

class Position:

    def __init__(self):
        self.contour=None
        self.area=None
        self.image=None
        self.center=None

    def SetPosition(self,image,threshold):
        # get the contour of this position
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh_img = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY_INV)
        contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
        self.contour= max(contours, key = cv2.contourArea)
        self.


    def GetDifference(self):
        pass


    def GetCorrelation(self):
        pass


    def Compare(self):
        pass

position=Position()
position.SetPosition(2,4)
print(position.area,"   ",type(position.area))