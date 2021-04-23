# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import urllib.request
import numpy as np
import argparse
import cv2
import imutils
import time

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
url='http://192.168.4.70:8080/shot.jpg'

# keep looping
while True:
	# Use urllib to get the image from the IP camera
	imgResp = urllib.request.urlopen(url)

	# Numpy to convert into a array
	imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)

	# Decode the array to OpenCV usable format
	frame = cv2.imdecode(imgNp,-1)

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	# find the largest contour in the mask, then use
	# it to compute the minimum enclosing circle and
	# centroid
	for c in cnts:
		((x, y), radius) = cv2.minEnclosingCircle(c)
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
	
# close all windows
cv2.destroyAllWindows()