import RPi.GPIO as GPIO


btn = 16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn, GPIO.IN)

while True:
    if (GPIO.input(btn) == 0):
        print("got here")
        
    else:
        print("we in here")
