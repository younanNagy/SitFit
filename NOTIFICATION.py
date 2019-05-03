from pynotifier import Notification
import winsound
from PIL import Image,ImageTk


def Warning(Title,Body,Icon_Path,Duration):
    Notification(
            title=Title,
            description=Body,
            #icon_path=warningph, # On Windows .ico is required, on Linux - .png
            duration=Duration,                              # Duration in seconds
            urgency=Notification.URGENCY_CRITICAL
    ).send()
 
    winsound.PlaySound("D://Users//samue//Documents//VSCode//SitFit//Alarm2.wav",winsound.SND_ASYNC)




def main():
    Warning("Warning","You have been sitting to close to the screen for X seconds",
            "D://Users//samue//Documents//VSCode//SitFit//Warn.png",20)

main()
