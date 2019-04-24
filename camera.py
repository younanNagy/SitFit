import numpy as np
import cv2

def brightness_contrast(img, alpha = 1.0, beta = 0):
	new_image = cv2.addWeighted(img,alpha,np.zeros(img.shape,img.dtype),0,beta)

	return new_image

def nothing(x):
    pass
cap = cv2.VideoCapture(cv2.CAP_DSHOW)
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
# fgbg = cv2.createBackgroundSubtractorMOG2()
cv2.namedWindow("Trackbars")
cv2.createTrackbar("min threshold", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("alpha", "Trackbars",100 , 300, nothing)
cv2.createTrackbar("beta", "Trackbars",50 , 100, nothing)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25,25))

while(True):
    thres = cv2.getTrackbarPos("min threshold", "Trackbars")
    alpha = cv2.getTrackbarPos("alpha", "Trackbars")
    beta = cv2.getTrackbarPos("beta", "Trackbars")

    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip( frame, 1 )
    # new_frame = cv2.convertScaleAbs(frame, alpha=alpha/100, beta = beta-50)
    new_frame = brightness_contrast(frame, alpha = alpha/100, beta = beta-50)
    # Our operations on the frame come here
    gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',new_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    




    blur = cv2.GaussianBlur(gray,(5,5),0)

    ret, thresh_img = cv2.threshold(blur,thres,255,cv2.THRESH_BINARY_INV)
    # thresh_img = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    thresh_img2 = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, kernel)

    contours =  cv2.findContours(thresh_img2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
    # max_area = 0
    # index =  0
    # for i in len(contours):
    #     area = cv2.contourArea(contours[i])
    #     if area > max_area:
    #         max_area = area
    #         index  = i
    if len(contours):
        c = max(contours, key = cv2.contourArea)
        M = cv2.moments(c)
        if (M["m00"] !=0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        cv2.drawContours(new_frame, [c], -1, (0,255,0), 3)
        cv2.circle(new_frame, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(new_frame, "area: "+str(cv2.contourArea(c)) , (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.putText(new_frame, "(" + str(cX) + "," + str(cY)+")", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # for c in contours:
    #     cv2.drawContours(new_frame, [c], -1, (0,255,0), 3)

     # Display the resulting frame
    cv2.imshow('frame',new_frame)
    cv2.imshow('thresh_img',thresh_img2)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # fgmask = fgbg.apply(frame)
    # # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    # cv2.imshow('frame',fgmask)
    # k = cv2.waitKey(30) & 0xff
    # if k == 27:
    #     break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()