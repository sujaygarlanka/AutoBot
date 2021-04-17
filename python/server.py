import asyncio
import websockets
import cv2
from pynput.keyboard import Key, Listener
from imutils.video import VideoStream
import threading, queue
import urllib.request
import numpy as np
import imutils

class Commands:
    @staticmethod
    async def send_command(command):
        uri = "ws://192.168.4.80:8000/websocket"
        async with websockets.connect(uri) as websocket:
            await websocket.send(command)
            response = await websocket.recv()
            print(response)

    @staticmethod
    def forward():
        asyncio.run(Commands.send_command('f'))

    @staticmethod
    def backward():
        asyncio.run(Commands.send_command('b'))

    @staticmethod
    def stop():
        asyncio.run(Commands.send_command('s'))

    @staticmethod
    def right():
        asyncio.run(Commands.send_command('r'))

    @staticmethod
    def left():
        asyncio.run(Commands.send_command('l'))

    @staticmethod
    def center():
        asyncio.run(Commands.send_command('c'))

class Keyboard_Controller:
    def __init__(self):
        pass

    def on_press(self, key):
        if key == Key.up:
            Commands.forward()
        elif key == Key.down:
            Commands.backward()
        elif key == Key.right:
            Commands.right()
        elif key == Key.left:
            Commands.left()

    def on_release(self, key):
        if key == Key.esc:
            # Stop listener
            return False
        if key == Key.up or key == Key.down:
            Commands.stop()
        elif key == Key.right or key == Key.left:
            Commands.center()

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
            for c in cnts:
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


def main(locations):
    while True:
        ball = locations.get()
        if len(ball) > 0:
            if ball[0][0] < 300:
                Commands.right()
            else:
                Commands.left()

if __name__ == '__main__':
    Commands.right()
    # camera = Camera()
    # x = threading.Thread(target=main, args=(camera.locations_stream,))
    # x.start()
    # camera.stream_ball_locations()
    # Keyboard_Controller().start()