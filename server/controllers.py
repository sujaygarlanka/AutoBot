import socket
import numpy as np

from pynput.keyboard import Key, Listener

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