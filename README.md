# Picamera_Timelapse


Dependency:

`pip3 install picamera`

`pip3 install crontab`

Usage: 

`main.py -l LENGTH -e EVENTLAST [-f FPS]`

Optional: 

`-f FPS (default (30))`


This script will create an HD video (3280x2464 default 30 fps) timelapse using the Raspberri Pi Camera v2. 

Tell the script how long you want the final video (-l) and how long the capture should last (-e) and it will calculate the interval between each captures.

You will find the video in the output directory (created by the script)

The frames will be in autopng, don't forget to clean the directory if you don't want to fill up the space on the sd card


