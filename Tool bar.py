from tkinter import *
from PIL import Image,ImageTk


from Position import *

cap = cv2.VideoCapture(cv2.CAP_DSHOW)

topWindowFlag =0
 
state =  "start"

current_pos = Position()
calibrated_pos = Position()

thres = 0
alpha = 0
beta = 0

#some thresholds
negative_area_threshold = -40
positive_area_threshold = 35
center_threshold = 10
xor_threshold = 8


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
 
master.geometry("100x300+300+300")

master.resizable(False,False)


exitImage = Image.open("D:\\projects\\0IMP_Projects\\Image Assignments\\Sit_fit\\SitFit\\exit3.png")
exitph = ImageTk.PhotoImage(exitImage)

calibrateImage = Image.open("D:\\projects\\0IMP_Projects\\Image Assignments\\Sit_fit\\SitFit\\calibrate1.png")
calibrateph = ImageTk.PhotoImage(calibrateImage)

blinkImage = Image.open("D:\\projects\\0IMP_Projects\\Image Assignments\\Sit_fit\\SitFit\\blink1.png")
blinkph = ImageTk.PhotoImage(blinkImage)

notificationImage = Image.open("D:\\projects\\0IMP_Projects\\Image Assignments\\Sit_fit\\SitFit\\notification1.png")
notificationph = ImageTk.PhotoImage(notificationImage)

streamImage = Image.open("D:\\projects\\0IMP_Projects\\Image Assignments\\Sit_fit\\SitFit\\stream1.png")
streamph = ImageTk.PhotoImage(streamImage)


#BUTTONS
exitButton = Button(master, text='Try', image=exitph, command=master.destroy)
createToolTip(exitButton,"exit")
exitButton.pack()

calibrateButton = Button(master, text='calibrate', image=calibrateph, command=lambda: topWindow())
createToolTip(calibrateButton,"calibrate your position")
calibrateButton.pack()

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

while True:
    master.update_idletasks()
    master.update()



    # global thres, alpha, beta
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip( frame, 1 )

    #print(state)
    if(state == "calibrate"):
        # print(thres)
        calibrated_pos.set_position(frame,thres,alpha,beta)
        if calibrated_pos.contour_flag :
           cv2.drawContours(calibrated_pos.colored_image, [calibrated_pos.contour], -1, (0,255,0), 3)

        cv2.imshow('frame',calibrated_pos.colored_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            state="running"
            cv2.destroyWindow('frame')


    elif(state == "running"):
        current_pos.set_position(frame,thres,alpha,beta)
        notification_type=calibrated_pos.compare(current_pos,
                                                 negative_area_threshold,
                                                 positive_area_threshold,
                                                 center_threshold,
                                                 xor_threshold)
        print(notification_type)




'''cv2.imshow('frame',current_pos.image)
        if cv2.waitKey(1) & 0xFF == ord('q')|z:
            cv2.destroyWindow('frame'''





