from tkinter import *
import PIL as pil
from ToolTip import *
import os





class GUI_class:

    def __init__(self):
        self.master = Tk("", "", "Toolbar", 1)
        self.master_destroyed = False
        self.top = None
        self.w = 55  # width for the Tk root
        self.h = 300  # height for the Tk root

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
        blinkImage = pil.Image.open(os.path.dirname(__file__) + "\\blink4.png")
        notificationImage = pil.Image.open(os.path.dirname(__file__) + "\\notification1.png")
        streamImage = pil.Image.open(os.path.dirname(__file__) + "\\stream1.png")
        pauseImage = pil.Image.open(os.path.dirname(__file__) + "\\pause.png")

        #Button Images
        self.exitph = pil.ImageTk.PhotoImage(exitImage)
        self.calibrate_blackph = pil.ImageTk.PhotoImage(calibrateBlackImage)
        self.calibrate_greenph = pil.ImageTk.PhotoImage(calibrateGreenImage)        
        self.blinkph = pil.ImageTk.PhotoImage(blinkImage)
        self.notificationph = pil.ImageTk.PhotoImage(notificationImage)
        self.streamph = pil.ImageTk.PhotoImage(streamImage)
        self.pauseph = pil.ImageTk.PhotoImage(pauseImage)


        #Buttons
        self.exitButton = Button(self.master, text='Try', image=self.exitph, command=self.exit2)
        self.calibrateButton = Button(self.master, text='calibrate', image=self.calibrate_blackph, command=self.calibrate)
        self.runButton = Button(self.master, text='Run/Pause', image=self.streamph, command=self.toggle)

        #Place the buttons on the main window
        self.calibrateButton.pack()
        self.runButton.pack()
        self.exitButton.pack()

        #define popup tip
        createToolTip(self.calibrateButton, "calibrate your position")
        createToolTip(self.runButton, "Run or pause SitFit")

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
            thresholdLabel = Label(self.top, text="threshold")
            thresholdLabel.pack()
            thresholdSlider = Scale(self.top, from_=0, to=200, orient=HORIZONTAL, command=self.update_threshold)
            thresholdSlider.set(50)
            # w.bind('<Button-1>', hide_me)
            thresholdSlider.pack()

            contrastLabel = Label(self.top, text="contrast")
            contrastLabel.pack()
            contrastSlider = Scale(self.top, from_=0, to=200, orient=HORIZONTAL, command=self.update_contrast)
            contrastSlider.set(50)
            contrastSlider.pack()

            brightnessLabel = Label(self.top, text="brightness")
            brightnessLabel.pack()
            brightnessSlider = Scale(self.top, from_=0, to=200, orient=HORIZONTAL, command=self.update_brightness)
            brightnessSlider.set(50)
            brightnessSlider.pack()
        else:
            self.topWindowFlag = 0
            self.top.destroy()





    def upon_select(self,widget, value):
        print("{}'s value is {}.".format(widget['text'], value))

    def update_threshold(self,val):

        self.thres = int(val)

    def update_contrast(self,val):

        self.alpha = int(val)

    def update_brightness(self,val):

        self.beta = int(val)

