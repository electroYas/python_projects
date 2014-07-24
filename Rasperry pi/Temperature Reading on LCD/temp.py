#!/bin/python2
import commands
import time
import i2c_lcd
	
def get_cpu_temp():
	tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
	cpu_temp = tempFile.read()
	tempFile.close()
	
	return float(cpu_temp)/1000
	 
def get_gpu_temp():
	gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace( 'temp=', '' ).replace( '\'C', '' )
	return  float(gpu_temp)

		

	
if __name__ == '__main__':
	
	try:
		lcd = i2c_lcd.Lcd()
		lcd.backlight()
		
		while(True):		
			lcd.lcd_puts("CPU temp:",0,0)
			lcd.lcd_puts("GPU temp:",0,1)
			temp1="{:.2f}".format(get_cpu_temp())
			temp2="{:.2f}".format(get_gpu_temp())
			lcd.lcd_puts(temp1,10,0)
			lcd.lcd_puts(temp2,10,1)	
			time.sleep(1)

	except KeyboardInterrupt:
		pass
		
