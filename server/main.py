import threading
import argparse

from camera import Camera
from controllers import Controller, Keyboard_Controller

def bot_control(locations):
    controller = Controller()
    empty_counter = 0
    while True:
        # 960 x 540
        location = locations.get(block=True)
        if len(location) > 0:
            location = location[0]
            # radius - 16, 173
            x = location[0]
            y = location[1]
            w = location[2]
            h = location[3]
            center = x + w/2
            size = w * h
            print(f"Center is {center}. Size is {size}.")
            if center < 480:
                controller.left()
            elif center > 480:
                controller.right()
            if size < 250000:
                controller.forward(220)
            elif size > 250000:
                controller.stop()
        else:
            empty_counter += 1
            if empty_counter > 10:
                controller.stop()
                controller.middle()            

# def keyboard_control(hello):
#     Keyboard_Controller().start()
                
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
        # camera = Camera()
        # camera.stream_yolov3_opencv()
    elif args['camera']:
        camera = Camera()
        # camera.stream_yolov3_personal()
        camera.stream_yolov3_opencv()
        # camera.stream_yolov5_ultralytics()
        # camera.stream_depth_map()
    else:
        camera = Camera()
        threading.Thread(target=bot_control, args=(camera.locations_stream,)).start()
        camera.stream_yolov3_opencv()

