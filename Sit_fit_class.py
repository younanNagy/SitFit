import numpy as np
import cv2
class Sit_fit:
    def __init__(self):
        calibrated_position=None
        current_postion=None
        
sit_fit=Sit_fit()
sit_fit.calibrated_image=cv2.imread("D:\\projects\\0IMP_Projects\\Image Assignments\\Sit_fit\\Capture.PNG")
print(type(sit_fit.calibrated_image))
cv2.imshow("test",sit_fit.calibrated_image)
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()