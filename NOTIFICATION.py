from pynotifier import Notification
import winsound
from PIL import Image,ImageTk

import os
def Warning(Title,Body,Icon_Path="",Duration=5):
    Notification(
            title=Title,
            description=Body,
            #icon_path=Icon_Path, # On Windows .ico is required, on Linux - .png
            duration=Duration,                              # Duration in seconds
            urgency=Notification.URGENCY_CRITICAL
    ).send()
 
    # winsound.PlaySound(os.path.dirname(__file__) + "\\Alarm2.wav",winsound.SND_ASYNC)



# def main():
#     Warning("Warning","You have been sitting to close to the screen for X seconds",)


# main()