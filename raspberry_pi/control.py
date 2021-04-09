import RPi.GPIO as GPIO
import time

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
    
def reverse(power):
    GPIO.output(BACK_POWER, GPIO.HIGH)
    GPIO.output(BACK_1, GPIO.LOW)
    GPIO.output(BACK_2, GPIO.HIGH)
    
def stop():
    GPIO.output(BACK_POWER, GPIO.LOW)
    GPIO.output(BACK_1, GPIO.LOW)
    GPIO.output(BACK_2, GPIO.LOW)
    
    
if __name__ == "__main__":
    forward(5)
    time.sleep(5)
    stop()

