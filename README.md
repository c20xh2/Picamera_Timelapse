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

:)


