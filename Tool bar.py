from tkinter import *
from PIL import Image,ImageTk

topWindowFlag =0

def upon_select(widget,value):
    print("{}'s value is {}.".format(widget['text'],value))

def print_value(val):
    print(val)

def topWindow():
    global topWindowFlag
    if topWindowFlag == 0:
        topWindowFlag =1
        top = Toplevel() 
        top.title('calibrate')
        thresholdLabel= Label(top, text="threshold")
        thresholdLabel.pack()    
        thresholdSlider = Scale(top, from_=0, to=200, orient=HORIZONTAL, command=print_value)
        thresholdSlider.set(50)
        #w.bind('<Button-1>', hide_me)
        thresholdSlider.pack()

        contrastLabel= Label(top, text="contrast")
        contrastLabel.pack()    
        contrastSlider = Scale(top, from_=0, to=200, orient=HORIZONTAL,command=print_value)
        contrastSlider.set(50)
        contrastSlider.pack()

        brightnessLabel= Label(top, text="brightness")
        brightnessLabel.pack() 
        brightnessSlider = Scale(top, from_=0, to=200, orient=HORIZONTAL,command=print_value)
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




exitImage = Image.open("exit3.png")
exitph = ImageTk.PhotoImage(exitImage)

calibrateImage = Image.open("calibrate1.png")
calibrateph = ImageTk.PhotoImage(calibrateImage)

blinkImage = Image.open("blink1.png")
blinkph = ImageTk.PhotoImage(blinkImage)

notificationImage = Image.open("notification1.png")
notificationph = ImageTk.PhotoImage(notificationImage)

streamImage = Image.open("stream1.png")
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

master.mainloop()




