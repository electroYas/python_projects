#!/bin/python2

#News feed monitor LCD 16x2 with I2C module
#save in local file for offline
#update if file size changes

import urllib
import re
import i2c_lcd
import time
import os
import RPi.GPIO as GPIO

local_path="./bbc_old.txt"
temp_path="/dev/shm/bbc_old.txt"
remote_path_list=[
"http://feeds.bbci.co.uk/news/world/asia/rss.xml",
"http://feeds.bbci.co.uk/news/technology/rss.xml",
"http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
"http://feeds.bbci.co.uk/news/world/rss.xml"
]
led_array = [4,17,18,22]	#[online status,searching status,display status,none]

def gpioSetup(leds):
	GPIO.setmode(GPIO.BCM)  
		
	for led in leds:
		GPIO.setup(led,GPIO.OUT)
		GPIO.output(led,0)
		
def lcd_intro():
	lcd.lcd_puts("*News feed monitor v1.1    Raspberry pi*",0,0)
	lcd.lcd_puts("Arch Linux ARM, Python2                 ",0,1)
	time.sleep(2)
	for i in range(0,24):
		lcd.display_shift()
		time.sleep(0.3)
	lcd.clear()
	
def file_write(path, text):
	f = open(path,'w')
	f.write(text)
	f.close()
	return os.path.getsize(path)

def display_news(headline_list, date_list):
	lcd.home()	
	lcd.lcd_putc('*')
	col=1
	index=0
	for header in headline_list:	
		print(header + " - " + str(date_list[index]))
		lcd.lcd_puts(date_list[index],0,1)	
		index=index+1
		lcd.setCursor(1,0)
		for ch in header:
			GPIO.output(led_array[2],1)
			lcd.lcd_putc(ch)
			GPIO.output(led_array[2],0)		
			if col>16:
				time.sleep(0.3)
			else:
				time.sleep(0.1)
				
			if col >= 15 :
				if(col % 2):
					lcd.display_shift()
					lcd.display_shift()
					
			if col>=35 and ch == ' ':
				col=0
				time.sleep(1)
				lcd.clear()
				lcd.home()
				continue
				
			if col>=39:
				col=0
				time.sleep(1)
				lcd.clear()
				lcd.home()
				continue
			
			col =col +1
		time.sleep(1)
		lcd.clear()
		lcd.lcd_putc('*')
		col=1
	time.sleep(5)
	
def main():
	
	lcd.backlight()	
	lcd_intro()
	gpioSetup(led_array)
	text=""
	while 1:	
		f_size=os.path.getsize(local_path)
		try:
			print("Getting news from remote server")
			for remote_path in remote_path_list:
				print("getting infomation from : "+ remote_path)
				text = text + urllib.urlopen(remote_path).read()
			print("done.")
			GPIO.output(led_array[0],1)
				
			f2_size = file_write(temp_path,text)
			
			if f_size == f2_size:
				print("local file up to date")
			else:
				print("Updating local file.")
				file_write(local_path,text)
			
				print("done.")
		except IOError:
			print("No connection!")
			GPIO.output(led_array[0],0)
			print("Getting news from local file")
			text = open(local_path).read()
			
	
		strings = text.split('<')	
		index=-1
		headline_list=[]
		date_list=[]
		headline_pattern=r'title>(.*)$'
		date_pattern="pubDate>(.*)$"
		for string in strings:
			GPIO.output(led_array[1],1)
			headline = re.search(headline_pattern,string)
			GPIO.output(led_array[1],0)
			date_news = re.search(date_pattern,string)	
			
			if headline :	
				temp = headline.group(1)
				if ("profile" not in temp and "VIDEO:" not in temp and "BBC News" not in temp) :
					index=index+1
					headline_list.insert(index,temp)
					date_list.insert(index,0)
					
			elif date_news:
				date_list.insert(index,date_news.group(1))
				
			
		display_news(headline_list,date_list)		
		
		print("reloading....")

if __name__ == '__main__':
	lcd=i2c_lcd.Lcd()
	main()			
		
		
	
			
	
