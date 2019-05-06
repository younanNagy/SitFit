import numpy as np
import cv2


class Position:

    def __init__(self):
        self.contour=None
        self.area=None
        self.image=None
        self.colored_image=None
        self.center=None
        self.contour_flag = False

    def set_position(self,image,threshold,alpha,beta):


        # get the contour of this position
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25,25))

        # new_frame = cv2.convertScaleAbs(image,alpha=alpha/100, beta = beta-50)
        new_frame = cv2.addWeighted(image,alpha/100,np.zeros(image.shape,image.dtype),0,beta)
        

        self.colored_image = new_frame
        gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh_img = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY_INV)
        thresh_img2 = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, kernel)

        ret,self.image=cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)

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

    def get_difference(self,current_position):

        diff=self.image^current_position.image
        diff = cv2.medianBlur(diff, 25)
        sum=np.sum(diff)
        normalized_diff=sum/(self.image.shape[0]*self.image.shape[1]*255)*100
        return normalized_diff


    def compare(self,current_position,negative_area_threshold,positive_area_threshold,center_threshold,xor_threshold):
        move_type="none"
        if current_position.contour_flag:
            area_difference=((self.area-current_position.area)/self.area)*100

            if area_difference<=negative_area_threshold:
                move_type="Move back a little bit, please"#"close"
            elif area_difference>=positive_area_threshold:
                move_type="Get closer to the screen, please"#far"
            else:
                center_difference=((self.center[0]-current_position.center[0])/self.image.shape[0])*100
                if abs(center_difference)>center_threshold:
                    if center_difference<0:
                        move_type="Move left a little bit, please"#"right"
                    else: #center_difference>0:
                        move_type ="Move right a little bit, please"# "left"

                else:
                    normalized_diff=self.get_difference(current_position)
                    if normalized_diff > xor_threshold:
                        move_type = "Stay in the upright position"#"uncomfortable_sit"
                    else:
                        move_type = "none"



        return move_type
