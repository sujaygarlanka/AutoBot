import cv2
from pynput.keyboard import Key, Listener
from imutils.video import VideoStream
import threading, queue
import urllib.request
import numpy as np
import imutils
import socket
import time
import argparse

class Controller:
   
    HOST = '192.168.4.106'  # The server's hostname or IP address
    PORT = 23        # The port used by the server

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))

    def _send_command(self, command, data):
        bytes = bytearray(str.encode(command))
        bytes.append(np.uint8(data))
        self.s.sendall(bytes)
        return repr(self.s.recv(1024))

    def left(self, power = 255):
        return self._send_command('L', power)

    def right(self, power = 255):
        return self._send_command('R', power)

    def middle(self):
        return self._send_command('M', 0)

    def forward(self, power = 255):
        return self._send_command('F', power)

    def backward(self, power = 255):
        return self._send_command('B', power)

    def stop(self):
        return self._send_command('S', 0)

    def cameraPosition(self, angle):
        return self._send_command('C', angle)

class Keyboard_Controller:
    def __init__(self):
        self.controller = Controller()
        self.controller.cameraPosition(130)
        self.cameraPosition = 30

    def on_press(self, key):
        if key == Key.up:
            self.controller.forward()
        elif key == Key.down:
            self.controller.backward()
        elif key == Key.right:
            self.controller.right()
        elif key == Key.left:
            self.controller.left()
        elif key == Key.caps_lock:
            self.cameraPosition = self.cameraPosition + 20
            print(self.cameraPosition)
            self.controller.cameraPosition(self.cameraPosition)
        elif key == Key.shift:
            self.cameraPosition = self.cameraPosition - 20
            self.controller.cameraPosition(self.cameraPosition)
            print(self.cameraPosition)

    def on_release(self, key):
        if key == Key.esc:
            # Stop listener
            return False
        if key == Key.up or key == Key.down:
            self.controller.stop()
        elif key == Key.right or key == Key.left:
            self.controller.middle()

    def start(self):
        # Collect events until released
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

class Camera():
    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)
    url = 'http://192.168.4.70:8080/shot.jpg'
    locations_stream = queue.Queue()

    def __init__(self):
        pass

    def stream_ball_locations(self):
        # keep looping
        while True:
            # Use urllib to get the image from the IP camera
            imgResp = urllib.request.urlopen(self.url)

            # Numpy to convert into a array
            imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)

            # Decode the array to OpenCV usable format
            frame = cv2.imdecode(imgNp,-1)

            # resize the frame, blur it, and convert it to the HSV
            # color space
            # frame size is 600 x 337 (w x h)
            frame = cv2.resize(frame, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(hsv, self.greenLower, self.greenUpper)
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
            locations_in_frame = []

            # for c in cnts:
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                # only proceed if the radius meets a minimum size
                if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                    cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                    locations_in_frame.append([x, y, radius])
            self.locations_stream.put(locations_in_frame)

            # show the frame to our screen
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break
            
        # close all windows
        cv2.destroyAllWindows()

def bot_control(locations):
    controller = Controller()
    while True:
        ball = locations.get()
        # radius - 16, 173
        if len(ball) > 0:
            if ball[0][0] < 250:
                controller.left()
            elif ball[0][0] > 350:
                controller.right()
            if ball[0][2] < 60:
                controller.forward()
            elif ball[0][2] > 60:
                controller.stop()
            
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--meltdown",
        help="meltdown and must turn off all motors", action='store_true')
    ap.add_argument("-k", "--keyboard",
        help="control the bot using the computer keyboard", action='store_true')
    ap.add_argument("-c", "--camera",
        help="show only camera output", action='store_true')
    args = vars(ap.parse_args())
    if args['meltdown']:
        controller = Controller()
        controller.stop()
        controller.middle()
    elif args['keyboard']:
        Keyboard_Controller().start()
    elif args['camera']:
        camera = Camera()
        camera.stream_ball_locations()
    else:
        camera = Camera()
        threading.Thread(target=bot_control, args=(camera.locations_stream,)).start()
        camera.stream_ball_locations()

