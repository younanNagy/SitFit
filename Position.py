import numpy as np
import cv2

class Position:

    def __init__(self):
        self.contour=None
        self.area=None
        self.image=None
        self.center=None
        self.contour_flag = False

    def set_position(self,image,threshold,alpha,beta):
        # get the contour of this position
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25,25))
        self.image=image
        new_frame = cv2.convertScaleAbs(image, alpha=alpha/100, beta = beta-50)
        self.image = new_frame
        gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh_img = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY_INV)
        thresh_img2 = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, kernel)
        contours = cv2.findContours(thresh_img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(contours):
            self.contour= max(contours, key = cv2.contourArea)
            self.area = cv2.contourArea(self.contour)
            self.contour_flag = True
            M=cv2.moments(self.contour)
            if (M["m00"] !=0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])            
                self.center=(cX, cY)
        else:
            self.contour_flag = False
            self.contour= None
            self.area = None
            self.center = None
            


    def get_difference(self):
        pass


    def get_correlation(self):
        pass


    def Compare(self):
        pass

# position=Position()
# position.SetPosition(2,4)
# print(position.area,"   ",type(position.area))
