from pynq.overlays.base import BaseOverlay
from pynq.lib.video import *
from pynq import PL
from PIL import Image as PIL_Image
import sys, cv2, math, copy
from time import time, sleep
import numpy as np
import asyncio
import datetime
import imutils
import threading 

#from appscript import app

program_is_running = True
key1 = 0
key2 = 0
key3 = 0
key4 = 0
key5 = 0
key6 = 0
key7 = 0
key8 = 0

PLAY_NOTHING = 0
PLAY_KEY_1   = 1
PLAY_KEY_2   = 2
PLAY_KEY_3   = 3 
PLAY_KEY_4   = 4
PLAY_KEY_5   = 5
PLAY_KEY_6   = 6
PLAY_KEY_7   = 7
PLAY_KEY_8   = 8

#count = 0
audio_out_state = PLAY_NOTHING
base = BaseOverlay("base.bit")
#initialize audio

audioout = base.audio

def start_audio():
	while 1:
		if (audio_out_state) == PLAY_NOTHING:
			pass 

		elif (audio_out_state) == PLAY_KEY_1:
			audioout.load("notes/Ab4.pdm")
			audioout.play()

		elif (audio_out_state) == PLAY_KEY_2:
			audioout.load("notes/Bb4.pdm")
			audioout.play()

		elif (audio_out_state) == PLAY_KEY_3:
			audioout.load("notes/Db4.pdm")
			audioout.play()

		elif (audio_out_state) == PLAY_KEY_4:
			audioout.load("notes/Eb4.pdm")
			audioout.play()

		elif (audio_out_state) == PLAY_KEY_5:
			audioout.load("notes/Gb4.pdm")
			audioout.play()

		elif (audio_out_state) == PLAY_KEY_6:
			audioout.load("notes/Ab4.pdm")
			audioout.play()

		elif (audio_out_state) == PLAY_KEY_7:
			audioout.load("notes/Bb4.pdm")
			audioout.play()
		
		elif (audio_out_state) == PLAY_KEY_8:
			audioout.load("notes/Db5.pdm")
			audioout.play()
	
		print("Woke up thread")	
		sleep(0.01)

# initialize output HDMI stream
my_mode = VideoMode(640, 480, 24)
hdmi_out = base.video.hdmi_out
hdmi_out.configure(my_mode, None ) 
hdmi_out.start()
print("Initialize output_HDMI")

# initialize input USB video capture
video_in = cv2.VideoCapture(0)
video_in.set(cv2.CAP_PROP_FRAME_WIDTH,  640 )
video_in.set(cv2.CAP_PROP_FRAME_HEIGHT, 480 )
print("Initialize video")
cap_region_x_begin=0.5  # start point/total width
cap_region_y_end=0.8  # start point/total width
threshold = 120  #  BINARY threshold
blurValue = 100  # GaussianBlur parameter
bgSubThreshold = 350

starttime = time()
# variables
isBgCaptured = 0   # bool, whether the background captured
triggerSwitch = False  # if true, keyborad simulator works
# initialize the first frame in the video stream
firstFrame = None

img_unpressed = cv2.imread("pics/unpressed.png",-1)
img_unpressed = cv2.resize(img_unpressed,(79,240),interpolation = cv2.INTER_AREA)
#img_unpressed_mask = img_unpressed[:,:,3]
#img_unpressed_mask_inv = cv2.bitwise_not(img_unpressed_mask)
#img_unpressed = img_unpressed[:,:,0:3]
unpressed_height,unpressed_width = img_unpressed.shape[:2]
img_un_alpha = img_unpressed[:,:,3]/255.0


img_pressed = cv2.imread("pics/pressed.png",-1)
#img_pressed_mask = img_pressed[:,:,3]
#img_pressed_mask_inv = cv2.bitwise_not(img_pressed_mask)
#img_pressed = img_pressed[:,:,0:3]
pressed_height,pressed_width = img_pressed.shape[:2]


try:
	# main loop- grab a frame from webcam, process it, push to HDMI
	print("Initialize video stream!")

	t = threading.Thread(target=start_audio)
	t.start()

	while program_is_running == True:
		start = time()
		retcode, frame_vga = video_in.read()
		# if the first frame is None, initialize it
		if firstFrame is None:
			outframe = hdmi_out.newframe()
			outframe[0:480, 0:640,:] = frame_vga[0:480,0:640,:]
			outframe1 = cv2.cvtColor(outframe, cv2.COLOR_RGB2GRAY)
			outframe1 = imutils.resize(outframe1,height=480,width=640)
			firstFrame = outframe
			continue
			
		elif retcode == True:
			outframe = hdmi_out.newframe()
			#count = count + 1
			
			key1 = 0
			key2 = 0
			key3 = 0
			key4 = 0
			key5 = 0
			key6 = 0
			key7 = 0
			key8 = 0


			# TODO FIXME process image here
			outframe[0:480, 0:640,:] = frame_vga[0:480,0:640,:]
			
			#outframe = imutils.resize(outframe, width=500)
			gray = cv2.cvtColor(outframe, cv2.COLOR_RGB2GRAY)
			gray = imutils.resize(gray,height=480,width=640)
			#gray_expanded = gray[:, :, np.newaxis]
			#gray = cv2.GaussianBlur(gray, (21, 21), 0)	
			
			#cv2.rectangle(outframe,(20,120),(119,360),(255,0,0),2)
			#mask1 = cv2.resize(unpressed_max, (unpressed_width,unpressed_height))
			#mask1_inv = cv2.resize(unpressed_mask_inv, (unpressed_width,unpressed_height))
			alpha_out = 1-img_un_alpha

			for i in range(8):
				for c in range(3):
					outframe[120:120+unpressed_height,18+75*i:18+unpressed_width+75*i,c] = (img_un_alpha * img_unpressed[:,:,c]+alpha_out*outframe[120:120+unpressed_height,18+75*i:18+unpressed_width+75*i,c])
			#cv2.rectangle(outframe,(120,120),(219,360),(255,0,0),2)
			#cv2.rectangle(outframe,(220,120),(319,360),(255,0,0),2)
			#cv2.rectangle(outframe,(320,120),(419,360),(255,0,0),2)
			#cv2.rectangle(outframe,(420,120),(519,360),(255,0,0),2)
			#cv2.rectangle(outframe,(520,120),(619,360),(255,0,0),2)
			
			# compute the absolute difference between the current frame and
			# first frame
			frameDelta = cv2.absdiff(outframe1, gray)
			#thresh = cv2.cvtColor(frameDelta, cv2.COLOR_RGB2GRAY)
			thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
			# dilate the thresholded image to fill in holes, then find contours
			# on thresholded image
			thresh = cv2.dilate(thresh, None, iterations=2)
			(im2, contours, hierarchy) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			 
			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			for c in contours:
				# if the contour is too small, ignore it
				if cv2.contourArea(c) < 10000:
					continue
				x, y, w, h = cv2.boundingRect(c)
				cv2.rectangle(outframe, (x, y), (x + w, y + h), (255, 0, 0), 2)
				M = cv2.moments(c)
				centroid_x = int(M['m10']/M['m00'])
				centroid_y = int(M['m01']/M['m00'])
				#print(centroid_x)
				#print(centroid_y)
				
				if(centroid_x > 20 and centroid_x < 95  and centroid_y > 180 and centroid_y < 420):
					key1 = 1
					cv2.rectangle(outframe,(20,120),(95,360),(0,255,255),2)
				elif(centroid_x > 95 and centroid_x < 170 and centroid_y > 180 and centroid_y < 420):
					key2 = 1
					cv2.rectangle(outframe,(95,120),(170,360),(255,0,255),2)
				elif(centroid_x > 170 and centroid_x < 245 and centroid_y > 180 and centroid_y < 420):
					key3 = 1
					cv2.rectangle(outframe,(170,120),(245,360),(255,255,0),2)
				elif(centroid_x > 245 and centroid_x < 320 and centroid_y > 180 and centroid_y < 420):
					key4 = 1
					cv2.rectangle(outframe,(245,120),(320,360),(255,0,0),2)
				elif(centroid_x > 320 and centroid_x < 395 and centroid_y > 180 and centroid_y < 420):
					key5 = 1
					cv2.rectangle(outframe,(320,120),(395,360),(0,255,0),2)
				elif(centroid_x > 395 and centroid_x < 470 and centroid_y > 160 and centroid_y < 430):
					key6 = 1
					cv2.rectangle(outframe,(395,120),(470,360),(0,255,255),2)
				elif(centroid_x > 470 and centroid_x < 545 and centroid_y > 160 and centroid_y < 430):
					key7 = 1
					cv2.rectangle(outframe,(470,120),(545,360),(255,0,255),2)
				elif(centroid_x > 545 and centroid_x < 620 and centroid_y > 160 and centroid_y < 430):
					key8 = 1
					cv2.rectangle(outframe,(545,120),(620,360),(255,255,0),2)
			hdmi_out.writeframe(outframe)	
			if key1 == 1:
				audio_out_state = PLAY_KEY_1

			elif key2 == 1:
				audio_out_state = PLAY_KEY_2

			elif key3 == 1:
				audio_out_state = PLAY_KEY_3

			elif key4 == 1:
				audio_out_state = PLAY_KEY_4

			elif key5 == 1:
				audio_out_state = PLAY_KEY_5

			elif key6 == 1:
				audio_out_state = PLAY_KEY_6
			
			elif key7 == 1:
				audio_out_state = PLAY_KEY_7
			
			elif key8 == 1:
				audio_out_state = PLAY_KEY_8

			else:
				audio_out_state = PLAY_NOTHING

		#you reached the end of video	
		else:
			print("Failed!")
			#break
		
		if (time()-starttime > 40 ):
			print("Timeout- terminate program")
			program_is_running = False

	# after 30s, close the stream
	print("Closing, goodbye!")
	video_in.release()
	hdmi_out.stop()
	del video_in
	del hdmi_out
	t.join()

	#del audioout
	sys.exit()

# TODO we wish this would work but jupyter is handling SIGINT 
except KeyboardInterrupt:
	print("Goodbye:keyboard")
	video_in.release()
	hdmi_out.stop()
	del hdmi_out
	del video_in
	t.join()
	#del audioout
	sys.exit()
	
except RuntimeError as e:
	print("Goodbye:runtime")
	print(e)
	video_in.release()
	hdmi_out.stop()
	del hdmi_out
	del video_in
	t.join()
	#del audioout
	sys.exit()
