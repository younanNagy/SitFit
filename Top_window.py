from tkinter import *
import PIL as pil
from ToolTip import *
import os





class Top_window:

    def __init__(self):
        self.blink_enable = True
        self.position_fit_enable = True
        self.timer_enable = True
        self.master = Tk("", "", "Toolbar", 1)
        self.master_destroyed = False
        self.top = None
        self.w = 50  # width for the Tk root
        self.h = 220  # height for the Tk root

        # get screen width and height
        self.ws = self.master.winfo_screenwidth()  # width of the screen
        self.hs = self.master.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk master window
        x = 0
        y = (self.hs / 2) - (self.h / 2)

        self.master.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.master.resizable(0, 0)
        self.master.overrideredirect(1)
        self.master.wm_attributes("-topmost", 1)

        exitImage = pil.Image.open(os.path.dirname(__file__) + "\\exit3.png")
        calibrateBlackImage = pil.Image.open(os.path.dirname(__file__) + "\\calibrate_black.png")
        calibrateGreenImage = pil.Image.open(os.path.dirname(__file__) + "\\calibrate_green.png")
        #notificationImage = pil.Image.open(os.path.dirname(__file__) + "\\notification1.png")
        streamImage = pil.Image.open(os.path.dirname(__file__) + "\\stream1.png")
        pauseImage = pil.Image.open(os.path.dirname(__file__) + "\\pause.png")
        blinkOnImage = pil.Image.open(os.path.dirname(__file__) + "\\blink_on.png")
        blinkOffImage = pil.Image.open(os.path.dirname(__file__) + "\\blink_off.png")
        chairOffImage = pil.Image.open(os.path.dirname(__file__) + "\\chair_off.png")
        chairOnImage = pil.Image.open(os.path.dirname(__file__) + "\\chair_on.png")
        timerOffImage = pil.Image.open(os.path.dirname(__file__) + "\\timer_off.png")
        timerOnImage = pil.Image.open(os.path.dirname(__file__) + "\\timer_on.png")

        #Button Images
        self.exitph = pil.ImageTk.PhotoImage(exitImage)
        self.calibrate_blackph = pil.ImageTk.PhotoImage(calibrateBlackImage)
        self.calibrate_greenph = pil.ImageTk.PhotoImage(calibrateGreenImage)        
        #self.notificationph = pil.ImageTk.PhotoImage(notificationImage)
        self.streamph = pil.ImageTk.PhotoImage(streamImage)
        self.pauseph = pil.ImageTk.PhotoImage(pauseImage)
        self.blinkonph = pil.ImageTk.PhotoImage(blinkOnImage)
        self.blinkoffph = pil.ImageTk.PhotoImage(blinkOffImage)
        self.chairoffph = pil.ImageTk.PhotoImage(chairOffImage)
        self.chaironph = pil.ImageTk.PhotoImage(chairOnImage)
        self.timeroffph = pil.ImageTk.PhotoImage(timerOffImage)
        self.timeronph = pil.ImageTk.PhotoImage(timerOnImage)

        #Buttons
        self.exitButton = Button(self.master, text='Exit', image=self.exitph, command=self.exit2)
        self.calibrateButton = Button(self.master, text='Start/Stop calibration', image=self.calibrate_blackph, command=self.calibrate)
        self.runButton = Button(self.master, text='Run/Pause', image=self.streamph, command=self.toggle)
        self.blinkButton = Button(self.master, text='Enable/Disable blinking', image=self.blinkonph, command=self.blink)
        self.chairButton = Button(self.master, text='Enable/Disable sitting fit', image=self.chaironph, command=self.chair)
        self.timerButton = Button(self.master, text='Enable/Disable timer', image=self.timeronph, command=self.timer)

        #Place the buttons on the main window
        self.calibrateButton.pack()
        self.runButton.pack()
        self.blinkButton.pack()
        self.chairButton.pack()
        self.timerButton.pack()
        self.exitButton.pack()

        #define popup tip
        createToolTip(self.calibrateButton, "Start/Stop calibration")
        createToolTip(self.runButton, "Run/Pause SitFit")
        createToolTip(self.exitButton, "Exit")
        createToolTip(self.blinkButton, "Enable/Disable blinking")
        createToolTip(self.chairButton, "Enable/Disable sitting posture")

        # some thresholds and flags for the GUI
        self.topWindowFlag=0
        self.state="start"
        self.thres = 0
        self.alpha = 0
        self.beta = 0

    def update(self):
        if self.master_destroyed == False:
            self.master.update_idletasks()
            self.master.update()

    def exit2(self):
        self.state = "exit"
        # print( self.topWindowFlag)
        # self.master_destroyed = True
        # self.master.destroy()
        # if self.topWindowFlag == 1:        
        #     self.topWindow()

    def timer(self):
        # to get the present state of the toggle button

        if self.timer_enable == True:
            self.timerButton.config(image=self.timeroffph)
            self.timer_enable = False
        else:
            self.timerButton.config(image=self.timeronph)
            self.timer_enable = True

    def chair(self):
        # to get the present state of the toggle button

        if self.position_fit_enable == True:
            self.chairButton.config(image=self.chairoffph)
            self.position_fit_enable = False
        else:
            self.chairButton.config(image=self.chaironph)
            self.position_fit_enable = True

    def blink(self):
        # to get the present state of the toggle button

        if self.blink_enable == True:
            self.blinkButton.config(image=self.blinkoffph)
            self.blink_enable = False
        else:
            self.blinkButton.config(image=self.blinkonph)
            self.blink_enable = True

    def toggle(self):
        # to get the present state of the toggle button

        if self.state == 'idle':
            self.runButton.config(image=self.pauseph)
            self.state = "running"
        elif self.state == 'running':
            self.runButton.config(image=self.streamph)
            self.state = "idle"

    def calibrate(self):
        # to get the present state of the toggle button

        if self.state != 'calibrate':
            self.calibrateButton.config(image=self.calibrate_greenph)
            self.topWindow()
            self.state = "calibrate"
        else:
            self.calibrateButton.config(image=self.calibrate_blackph)
            self.topWindow()
            self.state = "idle"

    def topWindow(self):
        if self.topWindowFlag == 0:
            self.top= Toplevel()
            self.topWindowFlag = 1
            # calculate x and y coordinates for the Tk master window
            x = self.w
            y = (self.hs / 2) - (self.h / 2)

            self.top.geometry('%dx%d+%d+%d' % (100, self.h, x, y))
            self.top.resizable(0, 0)
            self.top.overrideredirect(1)
            self.top.wm_attributes("-topmost", 1)
            # thresholdLabel = Label(self.top, text="threshold")
            # thresholdLabel.pack()
            thresholdSlider = Scale(self.top,showvalue = 0, from_=0, to=255, orient=HORIZONTAL, command=self.update_threshold,label = "Threshold")
            thresholdSlider.set(127)
            # w.bind('<Button-1>', hide_me)
            thresholdSlider.pack()

            # contrastLabel = Label(self.top, text="contrast")
            # contrastLabel.pack()
            contrastSlider = Scale(self.top,showvalue = 0, from_=0, to=200,orient=HORIZONTAL, command=self.update_contrast, label="Contrast")
            contrastSlider.set(100)
            contrastSlider.pack()

            # brightnessLabel = Label(self.top, text="brightness")
            # brightnessLabel.pack()
            brightnessSlider = Scale(self.top, showvalue = 0,from_=-255, to=255, orient=HORIZONTAL, command=self.update_brightness, label= "Brightness")
            brightnessSlider.set(0)
            brightnessSlider.pack()
        else:
            self.topWindowFlag = 0
            self.top.destroy()





    def upon_select(self,widget, value):
        print("{}'s value is {}.".format(widget['text'], value))

    def update_threshold(self,val):

        self.thres = int(val)

    def update_contrast(self,val):

        self.alpha = float(val)

    def update_brightness(self,val):

        self.beta = int(val)

