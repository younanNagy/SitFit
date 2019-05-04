from tkinter import *
from PIL import Image,ImageTk
from Position import *
from Blinking import *
from NOTIFICATION import *
import os


cap = cv2.VideoCapture(cv2.CAP_DSHOW)

topWindowFlag =0
 
state =  "running"

current_pos = Position()
calibrated_pos = Position()

thres = 0
alpha = 0
beta = 0

#blinking variables
COUNTER = 0   #counts number of frames of closed eyes
TOTAL = 0     #total number of blinks
flag_initialized = False    #flag to check if the detector and predictor are loaded
time_counter = 0
flag_start_count = False    #flag to check if someone is sitting
start_time = time.time()    #start timer for eye blinking
blinking_time_threshold = 60    #time to check the number of blinks


def upon_select(widget,value):
    print("{}'s value is {}.".format(widget['text'],value))

def update_threshold(val):
    global thres
    thres =int(val)
 
def update_contrast(val):
    global alpha
    alpha = int(val)

def update_brightness(val):
    global beta
    beta = int(val)      

def topWindow():
    global topWindowFlag
    global state
    if topWindowFlag == 0:
        state = "calibrate"
        topWindowFlag =1
        top = Toplevel() 
        top.resizable(False,False)
        top.title('calibrate')
        thresholdLabel= Label(top, text="threshold")
        thresholdLabel.pack()    
        thresholdSlider = Scale(top, from_=0, to=200, orient=HORIZONTAL, command=update_threshold)
        thresholdSlider.set(50)
        #w.bind('<Button-1>', hide_me)
        thresholdSlider.pack()

        contrastLabel= Label(top, text="contrast")
        contrastLabel.pack()    
        contrastSlider = Scale(top, from_=0, to=200, orient=HORIZONTAL,command=update_contrast)
        contrastSlider.set(50)
        contrastSlider.pack()

        brightnessLabel= Label(top, text="brightness")
        brightnessLabel.pack() 
        brightnessSlider = Scale(top, from_=0, to=200, orient=HORIZONTAL,command=update_brightness)
        brightnessSlider.set(50)
        brightnessSlider.pack()

def on_enter(widget,event):
        widget.configure(text="Hello world")
def on_leave(widget,enter):
        widget.configure(text="")

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


    
master = Tk("","","Toolbar",1)
w = 55 # width for the Tk root
h = 300 # height for the Tk root


# get screen width and height
ws = master.winfo_screenwidth() # width of the screen
hs = master.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk master window
x = 0
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
master.geometry('%dx%d+%d+%d' % (w, h, x, y))
 
#master.geometry("100x300+300+300")


master.resizable(0,0)
master.overrideredirect(1)
print( os.path.dirname(__file__))
#Setting images for icons of the tool bar
#required to change the path 
exitImage = Image.open( os.path.dirname(__file__)+"\\exit3.png")
exitph = ImageTk.PhotoImage(exitImage)

calibrateImage = Image.open( os.path.dirname(__file__)+"//calibrate1.png")
calibrateph = ImageTk.PhotoImage(calibrateImage)

blinkImage = Image.open( os.path.dirname(__file__)+"//blink4.png")
blinkph = ImageTk.PhotoImage(blinkImage)

notificationImage = Image.open( os.path.dirname(__file__)+"//notification1.png")
notificationph = ImageTk.PhotoImage(notificationImage)

streamImage = Image.open( os.path.dirname(__file__)+"//stream1.png")
streamph = ImageTk.PhotoImage(streamImage)

# pauseImage = Image.open( os.path.dirname(__file__)+"//pause.png")
# pauseph = ImageTk.PhotoImage(pauseImage)


#BUTTONS
#we use buttons ()
exitButton = Button(master, text='Try', image=exitph, command=master.destroy)
createToolTip(exitButton,"exit")
exitButton.pack()

calibrateButton = Button(master, text='calibrate', image=calibrateph, command=lambda: topWindow())
createToolTip(calibrateButton,"calibrate your position")
calibrateButton.pack()

#check boxes For ...

blinkFlag= BooleanVar()
blinkCheckButton = Checkbutton(master, text='Blinking-Check ON',image=blinkph,onvalue=True, offvalue=False, variable=blinkFlag
                               ,command= lambda: upon_select(blinkCheckButton,blinkFlag.get()))
createToolTip(blinkCheckButton,"blinking count on/off")
blinkCheckButton.pack()

notificationFlag = BooleanVar()
notificationCheckButton = Checkbutton(master, text='Notification ON',image=notificationph,onvalue=True, offvalue=False, variable=notificationFlag
                                      ,command= lambda: upon_select(notificationCheckButton,notificationFlag.get()))
createToolTip(notificationCheckButton,"notification on/off")
notificationCheckButton.pack()

streamFlag = BooleanVar()
streamCheckButton = Checkbutton(master, text='Stream ON',image = streamph,onvalue=True, offvalue=False, variable=streamFlag
                                ,command= lambda: upon_select(streamCheckButton,streamFlag.get()))
createToolTip(streamCheckButton,"stream on/off")
streamCheckButton.pack()

alg1Flag = BooleanVar()
alg1CheckButton = Checkbutton(master, text='Alg1',onvalue=True, offvalue=False, variable=alg1Flag
                              ,command= lambda: upon_select(alg1CheckButton,alg1Flag.get()))
createToolTip(alg1CheckButton,"alg1")
alg1CheckButton.pack()

alg2Flag = BooleanVar()
alg2CheckButton = Checkbutton(master, text='Alg2',onvalue=True, offvalue=False, variable=alg2Flag
                              ,command= lambda: upon_select(alg2CheckButton,alg2Flag.get()))
createToolTip(alg2CheckButton,"alg2")
alg2CheckButton.pack()

# print("before")
# master.mainloop()
# print("after")

## Testing only ##########################################################
# def nothing(x):
#     pass
# cv2.namedWindow("Trackbars")
# cv2.createTrackbar("min threshold", "Trackbars", 0, 255, nothing)
# cv2.createTrackbar("alpha", "Trackbars",100 , 300, nothing)
# cv2.createTrackbar("beta", "Trackbars",50 , 100, nothing)
#########################################################################
master.wm_attributes("-topmost", 1)

while True:
    master.update_idletasks()
    master.update()
 ## Testing only ##########################################################   
    # thres1 = cv2.getTrackbarPos("min threshold", "Trackbars")
    # alpha1 = cv2.getTrackbarPos("alpha", "Trackbars")
    # beta1 = cv2.getTrackbarPos("beta", "Trackbars")
#########################################################################

    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1 )
    
    #calibrate state to set the threshold , alpha and beta values
    if(state == "calibrate"):
        # print(thres)
        current_pos.set_position(frame,thres,alpha,beta)
        if current_pos.contour_flag == True:
            cv2.drawContours(current_pos.image, [current_pos.contour], -1, (0,255,0), 3)

        cv2.imshow('frame',current_pos.image)    #show the contoured image

    elif(state == "running"):
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
            
        
        # current_pos.set_position(frame,thres,alpha,beta)
        # notification_type=calibrated_pos.compare(current_pos,area_threshold,center_threshold,xor_threshold)





    



