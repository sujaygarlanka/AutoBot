import asyncio
import websockets
import cv2
from pynput.keyboard import Key, Listener

async def send_command(command):
    uri = "ws://192.168.4.80:8000/websocket"
    async with websockets.connect(uri) as websocket:
        await websocket.send(command)
        response = await websocket.recv()
        print(response)

# keyboard.on_press_key("f", lambda _:asyncio.run(send_command('f')))
# keyboard.on_press_key("s", lambda _:asyncio.run(send_command('s')))

def on_press(key):
    print(key)
    if key == Key.up:
        asyncio.run(send_command('f'))
    elif key == Key.down:
        asyncio.run(send_command('b'))
    elif key == Key.right:
        asyncio.run(send_command('r'))
    elif key == Key.left:
        asyncio.run(send_command('l'))

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False
    if key == Key.up:
        asyncio.run(send_command('s'))
    elif key == Key.down:
        asyncio.run(send_command('s'))
    elif key == Key.right:
        asyncio.run(send_command('c'))
    elif key == Key.left:
        asyncio.run(send_command('c'))

# Collect events until released
with Listener( on_press=on_press, on_release=on_release) as listener:
    listener.join()


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
    
