from tkinter import *
import PIL as pil
from ToolTip import *
import os





class GUI_class:

    def __init__(self):
        self.master = Tk("", "", "Toolbar", 1)
        w = 55  # width for the Tk root
        h = 300  # height for the Tk root

        # get screen width and height
        ws = self.master.winfo_screenwidth()  # width of the screen
        hs = self.master.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk master window
        x = 0
        y = (hs / 2) - (h / 2)

        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.master.resizable(0, 0)
        self.master.overrideredirect(1)
        self.master.wm_attributes("-topmost", 1)

        exitImage = pil.Image.open(os.path.dirname(__file__) + "\\exit3.png")
        calibrateImage = pil.Image.open(os.path.dirname(__file__) + "//calibrate1.png")
        blinkImage = pil.Image.open(os.path.dirname(__file__) + "//blink4.png")
        notificationImage = pil.Image.open(os.path.dirname(__file__) + "//notification1.png")
        streamImage = pil.Image.open(os.path.dirname(__file__) + "//stream1.png")
        pauseImage = pil.Image.open(os.path.dirname(__file__) + "//pause.png")

        #Button Images
        self.exitph = pil.ImageTk.PhotoImage(exitImage)
        self.calibrateph = pil.ImageTk.PhotoImage(calibrateImage)
        self.blinkph = pil.ImageTk.PhotoImage(blinkImage)
        self.notificationph = pil.ImageTk.PhotoImage(notificationImage)
        self.streamph = pil.ImageTk.PhotoImage(streamImage)
        self.pauseph = pil.ImageTk.PhotoImage(pauseImage)


        #Buttons
        self.exitButton = Button(self.master, text='Try', image=self.exitph, command=self.master.destroy)
        self.calibrateButton = Button(self.master, text='calibrate', image=self.calibrateph, command=lambda: self.topWindow())
        self.runButton = Button(self.master, text='Run/Pause', image=self.streamph, command=self.toggle)

        #Place the buttons on the main window
        self.exitButton.pack()
        self.calibrateButton.pack()
        self.runButton.pack()

        #define popup tip
        createToolTip(self.calibrateButton, "calibrate your position")
        createToolTip(self.runButton, "Run or pause SitFit")

        # some thresholds and flags for the GUI
        self.topWindowFlag=0
        self.state="running"
        self.thres = 0
        self.alpha = 0
        self.beta = 0

    def update(self):
        self.master.update_idletasks()
        self.master.update()

    def toggle(self):
        # to get the present state of the toggle button

        if self.state == 'idle':
            self.runButton.config(image=self.pauseph)
            self.state = "running"
        elif self.state == 'running':
            self.runButton.config(image=self.streamph)
            self.state = "idle"



    def topWindow(self):

        if self.topWindowFlag == 0:
            self.state = "calibrate"
            self.topWindowFlag = 1
            top = Toplevel()
            top.resizable(False, False)
            top.title('calibrate')
            thresholdLabel = Label(top, text="threshold")
            thresholdLabel.pack()
            thresholdSlider = Scale(top, from_=0, to=200, orient=HORIZONTAL, command=self.update_threshold)
            thresholdSlider.set(50)
            # w.bind('<Button-1>', hide_me)
            thresholdSlider.pack()

            contrastLabel = Label(top, text="contrast")
            contrastLabel.pack()
            contrastSlider = Scale(top, from_=0, to=200, orient=HORIZONTAL, command=self.update_contrast)
            contrastSlider.set(50)
            contrastSlider.pack()

            brightnessLabel = Label(top, text="brightness")
            brightnessLabel.pack()
            brightnessSlider = Scale(top, from_=0, to=200, orient=HORIZONTAL, command=self.update_brightness)
            brightnessSlider.set(50)
            brightnessSlider.pack()





    def upon_select(self,widget, value):
        print("{}'s value is {}.".format(widget['text'], value))

    def update_threshold(self,val):

        self.thres = int(val)

    def update_contrast(self,val):

        self.alpha = int(val)

    def update_brightness(self,val):

        self.beta = int(val)

