import RPi.GPIO as GPIO
import time
import tornado.web
import tornado.websocket

BACK_1 = 14
BACK_2 = 15
BACK_POWER = 18

FRONT_1 = 2
FRONT_2 = 3
FRONT_POWER = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BACK_1, GPIO.OUT)
GPIO.setup(BACK_2, GPIO.OUT)
GPIO.setup(BACK_POWER, GPIO.OUT)


def left(power):
    GPIO.output(FRONT_POWER, GPIO.HIGH)
    GPIO.output(FRONT_1, GPIO.LOW)
    GPIO.output(FRONT_2, GPIO.HIGH)
    
def right(power):
    GPIO.output(FRONT_POWER, GPIO.HIGH)
    GPIO.output(FRONT_1, GPIO.HIGH)
    GPIO.output(FRONT_2, GPIO.LOW)
    
def center():
    GPIO.output(FRONT_POWER, GPIO.LOW)
    GPIO.output(FRONT_1, GPIO.LOW)
    GPIO.output(FRONT_2, GPIO.LOW)

def forward(power):
    GPIO.output(BACK_POWER, GPIO.HIGH)
    GPIO.output(BACK_1, GPIO.HIGH)
    GPIO.output(BACK_2, GPIO.LOW)
    
def backward(power):
    GPIO.output(BACK_POWER, GPIO.HIGH)
    GPIO.output(BACK_1, GPIO.LOW)
    GPIO.output(BACK_2, GPIO.HIGH)
    
def stop():
    GPIO.output(BACK_POWER, GPIO.LOW)
    GPIO.output(BACK_1, GPIO.LOW)
    GPIO.output(BACK_2, GPIO.LOW)
    
class WebSocket(tornado.websocket.WebSocketHandler):

    def on_message(self, message):
        """Evaluates the function pointed to by json-rpc."""
        if message == 'f':
                forward(0)
                self.write_message("forward")
        elif message == 'b':
                backward(0)
                self.write_message("backward")
        elif message == 's':
                stop()
                self.write_message("stop")
        elif message == 'r':
                right(0)
                self.write_message("right")
        elif message == 'l':
                left(0)
                self.write_message("left")
	elif message == 'c':
		center()
		self.write_message('center')
	else:
		self.write_message('command not recognized')
    
if __name__ == "__main__":
    handlers = [(r"/websocket", WebSocket)]
    application = tornado.web.Application(handlers)
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

