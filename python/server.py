import asyncio
import websockets
import cv2
from pynput.keyboard import Key, Listener

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

if __name__ == '__main__':
    Keyboard_Controller().start()



# import numpy as np
# import urllib.request
# import cv2


# # Replace the URL with your own IPwebcam shot.jpg IP:port
# url='http://192.168.4.101:8080/shot.jpg'


# while True:
#     # Use urllib to get the image from the IP camera
#     imgResp = urllib.request.urlopen(url)

#     # Numpy to convert into a array
#     imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)

#     # Decode the array to OpenCV usable format
#     img = cv2.imdecode(imgNp,-1)


#     # put the image on screen
#     cv2.imshow('IPWebcam',img)
    
#     # Program closes if q is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
    
