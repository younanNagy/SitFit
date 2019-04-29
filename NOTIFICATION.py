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

    winsound.PlaySound("Alarm.wav",winsound.SND_ASYNC)




def main():
    Warning("Warning","You have been sitting to close to the screen for X seconds",
            "E://4th comp/Second Term/Image processing/project GUI/Warning.ico",20)

main()
