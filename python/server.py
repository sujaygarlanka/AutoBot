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
        asyncio.run(send_comdmand('b'))
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

# if __name__=='__main__':
#     while True:
#         key = cv2.waitKey(1) & 0xFF

#         # if the 'ESC' key is pressed, Quit
#         if key == 27:
#             quit()
#         if key == 0:
#             print("up")
#         elif key == 1:
#             print("down")
#         elif key == 2:
#             print("left")
#         elif key == 3:
#             print("right")
#         # 255 is what the console returns when there is no key press...
#         elif key != 255:
#             print(key)