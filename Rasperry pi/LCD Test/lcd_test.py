#!/bin/python2

import smbus
import time
import i2c_lcd

def main():
	lcd = i2c_lcd.Lcd()
	lcd.backlight()
	lcd.lcd_puts("Counter",3,0)
	counter =0
	while 1:
		lcd.lcd_puts("%d" % counter,1,1)
		time.sleep(1)
		counter=counter+1
	
	
	
	
if __name__ == '__main__':
	try:
		main()
		
	except KeyboardInterrupt:
		pass
