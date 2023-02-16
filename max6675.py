#import RPi.GPIO as GPIO
#from Adafruit_GPIO.GPIO as GPIO
import digitalio
import board
import time
import busio

#GPIO.setmode(GPIO.BOARD)
#PIO.setwarnings(False)

# set pin number for communicate with MAX6675
def set_pin (UNIT):
    global sck
    global so
    global cs
    global unit
    global spi

    unit = UNIT
    
    print(board.SPI_CS0)
    print(board.P24)

    print(board.MISO)
    print(board.P21)

    print(board.SCLK)
    print(board.P23)

    #spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)

    #GPIO.setup(CS, GPIO.OUT, initial = GPIO.HIGH)
    cs = digitalio.DigitalInOut(board.P26)
    cs.direction = digitalio.Direction.OUTPUT
    cs.value = True
    
    #GPIO.setup(SCK, GPIO.OUT, initial = GPIO.LOW)
    sck = digitalio.DigitalInOut(board.P23)
    sck.direction = digitalio.Direction.OUTPUT
    sck.value = False

    #GPIO.setup(SO, GPIO.IN)
    so = digitalio.DigitalInOut(board.P21)
    so.direction = digitalio.Direction.INPUT
    

def read_temp():
    
    #GPIO.output(cs, GPIO.LOW)
    cs.value = False
    time.sleep(0.002)
    #GPIO.output(cs, GPIO.HIGH)
    cs.value = True
    time.sleep(0.22)

    #GPIO.output(cs, GPIO.LOW)
    cs.value = False
    #GPIO.output(sck, GPIO.HIGH)
    sck.value = True
    time.sleep(0.001)
    #GPIO.output(sck, GPIO.LOW)
    sck.value = False
    Value = 0
    for i in range(11, -1, -1):
        #GPIO.output(sck, GPIO.HIGH)
        sck.value = True
        #Value = Value + (GPIO.input(so) * (2 ** i))
        Value = Value + (so.value * (2 ** i))
        #GPIO.output(sck, GPIO.LOW)
        sck.value = False

    #GPIO.output(sck, GPIO.HIGH)
    sck.value = True
    #error_tc = GPIO.input(so)
    error_tc = so.value
    #GPIO.output(sck, GPIO.LOW)
    sck.value = False

    for i in range(2):
        #GPIO.output(sck, GPIO.HIGH)
        sck.value = True
        time.sleep(0.001)
        #GPIO.output(sck, GPIO.LOW)
        sck.value = False

    #GPIO.output(cs, GPIO.HIGH)
    cs.value = True

    if unit == 0:
        temp = Value
    if unit == 1:
        temp = Value * 0.25
    if unit == 2:
        temp = Value * 0.25 * 9.0 / 5.0 + 32.0

    if error_tc != 0:
        return -cs
    else:
        return temp


