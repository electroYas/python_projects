#!/bin/python2

#News feed monitor LCD 16x2 with Arduino
#save in local file for offline
#update if file size changes

import urllib
import re
import time
import os
import serial


local_path="./bbc_old.txt"
temp_path="/dev/shm/bbc_old.txt"
remote_path_list=[
"http://feeds.bbci.co.uk/news/world/asia/rss.xml",
"http://feeds.bbci.co.uk/news/technology/rss.xml",
"http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
"http://feeds.bbci.co.uk/news/world/rss.xml"
]
ser = serial.Serial('/dev/ttyACM0', 9600)

def file_write(path, text):
	f = open(path,'w')
	f.write(text)
	f.close()
	return os.path.getsize(path)


def display_news(headline_list, date_list):
  index=0
  time.sleep(2)
  for header in headline_list:
    print(header + " - " + str(date_list[index]))
    ser.write(header+'\n')
    index=index+1
    time.sleep(10)
  
  
def main():
	
	text=""
	while 1:	
		f_size=os.path.getsize(local_path)
		try:
			print("Getting news from remote server")
			for remote_path in remote_path_list:
				print("getting infomation from : "+ remote_path)
				text = text + urllib.urlopen(remote_path).read()
			print("done.")
				
			f2_size = file_write(temp_path,text)
			
			if f_size == f2_size:
				print("local file up to date")
			else:
				print("Updating local file.")
				file_write(local_path,text)
			
				print("done.")
		except IOError:
			print("No connection!")
		
			print("Getting news from local file")
			text = open(local_path).read()
			
	
		strings = text.split('<')	
		index=-1
		headline_list=[]
		date_list=[]
		headline_pattern=r'title>(.*)$'
		date_pattern="pubDate>(.*)$"
		for string in strings:
			
			headline = re.search(headline_pattern,string)
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
	main()			
		
		
	
			
	
