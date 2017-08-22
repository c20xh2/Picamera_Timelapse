import time
import subprocess
import os
import sys
import argparse
from picamera import PiCamera
from crontab import CronTab



def videoexport(fps, finalname, created, outputpath, savepath):
	print('\n[+] Creating video file please wait... ')
	FNULL = open(os.devnull, 'w')
	subprocess.call(['avconv', '-r', str(fps), '-i', str(savepath) + '/%d.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(outputpath) + str(finalname)], stdout=FNULL, stderr=subprocess.STDOUT)
	print('\n[!] Congrats ! Filename: ' + str(finalname))

# Argument parsing

parser = argparse.ArgumentParser()
parser.add_argument('-l', dest='length', help='Length of the output video (in seconds)', type=int, required=True)
parser.add_argument('-e', dest='eventlast', help='How long will the event last (in hours)', type=int, required=True)
parser.add_argument('-f', dest='fps', help='frame per seconds', type=int, required=False, default=30)
args = parser.parse_args()


fps = args.fps
length = args.length
eventlast = args.eventlast

# Get video info

created = time.strftime('%y%m%d%H%M')
created = created.replace('/', '')
finalname = (str(created) + '-' + str(length) + '-' + str(eventlast) + '.mp4' )



# make sure savepath exist
dirpath = time.strftime('%y%m%d%H%M')
savepath = 'autopng/' + str(dirpath)
outputpath = 'output/'
logpath = 'logs/'
try: 
    os.makedirs(savepath)
except OSError:
    if not os.path.isdir(savepath):
        raise
try: 
    os.makedirs(outputpath)
except OSError:
    if not os.path.isdir(outputpath):
        raise
try: 
    os.makedirs(logpath)
except OSError:
    if not os.path.isdir(logpath):
        raise
# Video specs calculations
nbframe = fps * length
eventlastsec = eventlast * 3600
interval = eventlastsec / nbframe

i = 0


print ("\n" *200)

print ("###### Validations ######")

print ("\n[+] Output file name: " + str(finalname))
print (" [|] Event length: " + str(eventlast) + " h.")
print (" [|] Final Video length: " + str(length) + " sec.")

print ("\n[+] Video specs: ")
print (" [|] Fps: " + str(fps) +".")
print (" [|] Number of frames: " + str(nbframe) + ".") 
print (" [|] Interval between shots: " + str(interval) + " sec.")
print ("")

launch = input('[*] Ready ? (y/n) : ')

if launch == ('n'):
	print ('\nAbording Capture...')

elif launch == ('y'):
	launched = time.strftime('%c')
	cron = input('\n[*] Schedule task ? (y/n) : ')
	if cron == ('y'):
		print ('\n')
		dir_path = os.path.dirname(os.path.realpath(__file__))
		cronuser = input('[*] Please enter username: ')
		cronwhen = input('[*] Launch time Hours:Minute (use 24h format) :')

		hour = cronwhen.split(':')[0]
		minutes = cronwhen.split(':')[1]

		my_cron = CronTab(user=cronuser)
		job = my_cron.new(command='cd ' + str(dir_path) + " && " + "python3 auto.py -u " + str(username) + " -p " + str(password) + ' -t ' + str(protocol) + ' -c ' + str(camera) +  ' -l ' + str(length) + ' -e ' + str(eventlast) + ' -n ' + str(correction) + ' -f ' + str(fps), comment=launched)
		job.hour.on(hour)
		job.minute.on(minutes)
		my_cron.write()
		print('\nThank you... Recording will start at: ' + str(cronwhen))
		sys.exit()

	print("Starting process...")

	with open(str(logpath) + str(created), 'a') as logfile:
		log = ('\n' + str(finalname) + '\nFps:' + str(fps) + '\nEventlast:' + str(eventlast) + '\nFinalVideo:' + str(length) + '\nNbframe:' + str(nbframe) + '\nInterval:' + str(interval))
		logfile.write(log)
		logfile.close()

	while (i < nbframe):
		try:
			# Get info for how long left
			frameleft = nbframe - i
			timeleft = frameleft * interval / 60
			timeleft = round(timeleft, 0)
			# Grab the frame
			camera = PiCamera()
			camera.resolution = (1920, 1080)
			filename  = savepath + '/' + str(i) + '.png'
			time.sleep(interval)
			time.sleep(0.5)
			camera.capture(filename, format='png')
			camera.close()
			print ("\n" * 200)
			print ("[+] Current time: " + time.strftime("%c"))
			print (" [|] Process started: " + str(launched))
			print (" [|] Event length: " + str(eventlast) + " h.")
			print (" [|] Final Video length: " + str(length) + " sec.")
			print ("\n[+] Video specs: ")
			print (" [|] Fps: " + str(fps) +".")
			print (" [|] Number of frames: " + str(nbframe) + ".") 
			print (" [|] Interval between shots: " + str(interval) + " sec.")
			print ("")
			print ("\n[+] " + str(i) + "/" + str(nbframe) +" Frames captured")
			print (" [|] " + str(timeleft) + " minutes left")
			i = i + 1
		except Exception as e:
			print (e)
		except KeyboardInterrupt:
			print ("\n[!] Keyboard Interrupt ! ")
			videoexport(fps, finalname, created, outputpath, savepath)
			sys.exit()
	# Capture is over, putting all the images together to create video file
	videoexport(fps, finalname, created, outputpath, savepath)
	print("\n[!] Success !!!")
else:
	print ('\nAbording Capture...')

