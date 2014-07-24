import RPi.GPIO as GPIO
import time

led1=4
led2=17
		
def blink():
	GPIO.output(led1,1)
	GPIO.output(led2,0)
	time.sleep(1)
	GPIO.output(led2,1)
	GPIO.output(led1,0)
	time.sleep(1)

if __name__ == '__main__':
	try:
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(led1,GPIO.OUT)
		GPIO.setup(led2,GPIO.OUT)
		while 1:
			blink()		
	except KeyboardInterrupt:
		GPIO.cleanup()
		
	
