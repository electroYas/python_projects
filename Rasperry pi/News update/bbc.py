import urllib
import re
import i2c_lcd
import time
import os

def display_shift():
	displayshift = lcd.LCD_DISPLAYMOVE | lcd.LCD_MOVELEFT
	lcd.command(lcd.LCD_CURSORSHIFT | displayshift)


lcd=i2c_lcd.Lcd()
lcd.backlight()

local_path="./bbc_old.txt"
temp_path="/dev/shm/bbc_old.txt"
remote_path="http://feeds.bbci.co.uk/news/world/asia/rss.xml"

while 1:	
	f_size=os.path.getsize(local_path)
	try:
		print("Getting news from remote server")
		source = urllib.urlopen(remote_path).read()
		text = source
		print("done.")
		f = open(temp_path,'w')
		f.write(text)
		f.close()
		f2_size=os.path.getsize(temp_path)
		if f_size == f2_size:
			print("local file up to date")
		else:
			print("Updating local file.")
			f = open(local_path,'w')
			f.write(text)
			f.close()
			print("done.")
	except IOError:
		print("No connection!")
		print("Getting news from local file")
		source = open(local_path).read()
		text = source

	strings = text.split('<')	
	index=0
	headline_list=[]
	for string in strings:
		headline_pattern=r'title>(.*)$'
		headline = re.search(headline_pattern,string)
		
		if headline :	
			temp = headline.group(1)
			if ("profile" not in temp and "VIDEO:" not in temp) :
				headline_list.insert(index,temp)
				index=index+1
				
	lcd.home()	
	col=0
	for header in headline_list:	
		for ch in header:
			lcd.lcd_putc(ch)
			time.sleep(0.3)
			if col >= 15 :
				display_shift()
			if col>=25 and ch == ' ':
				col=0
				time.sleep(1)
				lcd.clear()
				continue
			col =col +1
		time.sleep(1)
		lcd.clear()
		lcd.lcd_putc('*')
		col=0
		
	time.sleep(5)
	print("reloading....")
		
		
		
	
			
	
