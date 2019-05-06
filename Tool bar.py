from tkinter import *
from Position import *
#from Blinking import *
from NOTIFICATION import *
import time
from GUI_class import *

import os



def main():

    cap = cv2.VideoCapture(cv2.CAP_DSHOW)

    topWindowFlag = 0

    lock=0

    current_pos = Position()
    calibrated_pos = Position()


    # Position Sit thresholds
    negative_area_threshold = -40
    positive_area_threshold = 35
    center_threshold = 10
    xor_threshold = 7

    '''
    #blinking variables
    COUNTER = 0   #counts number of frames of closed eyes
    TOTAL = 0     #total number of blinks
    flag_initialized = False    #flag to check if the detector and predictor are loaded
    time_counter = 0
    flag_start_count = False    #flag to check if someone is sitting
    start_time = time.time()    #start timer for eye blinking
    blinking_time_threshold = 60    #time to check the number of blinks
    '''




    window=GUI_class()

    old_notification_type="none"
    start_time_for_position_fit=time.time()
    start_time_for_blink=time.time()
    running_state_start_time=time.time()

    while True:
        #master.update_idletasks()
        #master.update()
        window.update()



        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1 )
        #print(window.state)
        #calibrate state to set the threshold , alpha and beta values
        if(window.state == "calibrate"):
            calibrated_pos.set_position(frame, window.thres, window.alpha, window.beta)
            #draw the contour on the captured frame
            if calibrated_pos.contour_flag:
                cv2.drawContours(calibrated_pos.colored_image, [calibrated_pos.contour], -1, (0, 255, 0), 3)

            # Guide cross
            cv2.line(calibrated_pos.colored_image, (int(calibrated_pos.colored_image.shape[1]/2), 0),
                     (int(calibrated_pos.colored_image.shape[1]/2),calibrated_pos.colored_image.shape[0]), (0, 0, 255), 1)
            cv2.line(calibrated_pos.colored_image, (0, int(calibrated_pos.colored_image.shape[0]/2)),
                     (calibrated_pos.colored_image.shape[1], int(calibrated_pos.colored_image.shape[0]/2)), (0, 0, 255),1)


            cv2.imshow('frame', calibrated_pos.colored_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                window.state = "running"


        elif(window.state == "running"):

            cv2.destroyWindow('frame')

            running_state_end_time=time.time()
            if int(running_state_end_time-running_state_start_time)>60*60:
               pass
            '''
            if(window.blink_enable):
                #blinking part
                
                #initializing face detector and predictor
                if flag_initialized == False:
                    # print("initializing face detector...")
                    detector = dlib.get_frontal_face_detector()
                    # print("initializing face predictor...")
                    predictor = dlib.shape_predictor( os.path.dirname(__file__)+"\\shape_predictor_68_face_landmarks.dat")
                    # print("done initializing all")
                    flag_initialized = True
                else:
                    
                    end_time = time.time()
                    current_time = end_time - start_time   #calculate timer for counting blinks in one min
                    if flag_start_count == True:
                        time_counter = end_time - start_time_human  #calculate time for measuring if the person is sitting or not
                        if int(time_counter) >= 15:
                            # print("no one is sitting in front of the computer !!!!!")
                            Warning("Detection Error" , "No one is sitting in front of the computer")
                    
                    if int(current_time) >= blinking_time_threshold:   
                        if TOTAL < 15:  #check if the min number of blinks is 15
                            # print("warning blink more !!!!")
                            Warning("Blink More" , "Blinking helps protect your eyes from dehydration")
                        COUNTER = 0
                        TOTAL = 0
                        start_time = time.time()
        
                    frame = imutils.resize(frame, width=450)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    #get gray image 
        
                    rects = detector(gray, 0)   #get detected face
                    
                    flag_blink , COUNTER , ear , TOTAL = blink_detector(frame , gray , rects , COUNTER , predictor , TOTAL)
                    
                    if ear == 0 and flag_start_count == False: #check if someone is sitting in front of the computer
                        flag_start_count = True  #no one is sitting
                        start_time_human = time.time()  #start timer if no one is sitting 
                    elif ear != 0 :
                        flag_start_count = False
                        time_counter = 0
        
                    cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),    #show the number of blinks on the stream
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)       
                    cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),   #show the ear on the streamed video
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
                    # show the frame
                    
                    cv2.imshow("Frame", frame)
                    
                    ########################################################################################
                    end_time_for_blink=time.time()
                    if ear==0 and !lock:
                        start_time_for_blink=time.time()
                        lock=1
                    
                    if ear != 0:
                        lock=0
                    if int(end_time_for_blink-start_time_for_blink)>60*60 and there_is_eye_contour==0:
                         Warning("Unco" ,notification_type)
                         start_time_for_blink = time.time()
                         lock=0
                    ##############################################################################################     
                    '''
            #if(window.position_fit_enable):
            current_pos.set_position(frame, window.thres, window.alpha, window.beta)
            notification_type = calibrated_pos.compare(current_pos,
                                                       negative_area_threshold,
                                                       positive_area_threshold,
                                                       center_threshold,
                                                       xor_threshold)


            # timer for notifications
            print(notification_type)
            if notification_type!=old_notification_type and notification_type!="none":
                old_notification_type=notification_type
                start_time_for_position_fit=time.time()
            end_time_for_position_fit=time.time()
            if int(end_time_for_position_fit-start_time_for_position_fit)>5 and notification_type!="none":

                Warning("Uncomfortable Position Detected" ,notification_type)
                start_time_for_position_fit = time.time()


main()
