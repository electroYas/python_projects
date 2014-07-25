import webkit
import gtk
import i2c_lcd
import time
import re

def get_html():
	#print("Debug:get_html()")
	view.execute_script('oldtitle=document.title;document.title=document.documentElement.innerHTML;')
	html = view.get_main_frame().get_title()
	view.execute_script('document.title=oldtitle;')
	time.sleep(1)
	return html

def finish_load(view,frame):
	global string1
	#print("Debug:finish_load(view,frame)")
	time.sleep(1)
	string1=get_html()
	#print(string1)
	gtk.main_quit()	
	

string1=""
lcd = i2c_lcd.Lcd()
lcd.backlight()
window = gtk.Window()
view = webkit.WebView()	

print("opening...")
view.open('http://localhost:9091')
print("connecting...")
view.connect('load-finished',finish_load)
window.add(view)

while 1:
	
	gtk.main()
	view.reload()
	#print("reloading...")
	stringList=string1.split('<')
	
	names_list=[]
	down_speed_list=[]
	up_speed_list=[]
	progress_list=[]
	index=-1
	#print("Debug:String pattern search")
	for string in stringList:
		#print(string)
		name = re.search(r'div class="torrent_name">(.*)$',string)
		temp1 = re.search(r'div class="torrent_peer_details">(.*)$',string)
		temp2 = re.search(r'div class="torrent_progress_details">(.*)$',string)
		try:
			if name :
				names_list.append(name.group(1))
				index = index +1
				down_speed_list.insert(index,0)
				up_speed_list.insert(index,0)
				progress_list.insert(index,100)
				
			if temp1 and index>=0:				
				speed = re.search(r'(\d*?) kB/s .*? (\d*?) kB/s',temp1.group(1))
				down_speed_list.insert(index,speed.group(1))#download
				up_speed_list.insert(index,speed.group(2))#upload
				
			if temp2 and index>=0:
				progress=re.search(r'(\d*?.\d)\%',temp2.group(1))
				progress_list.insert(index,progress.group(1))#progress
				
		except AttributeError:
			pass
	i=0	
	for result in names_list:
		lcd.clear()
		lcd.lcd_puts(result,0,0)
		lcd.lcd_puts("D:   kB/s",0,1)
		lcd.lcd_puts(str(down_speed_list[i]),2,1)
		lcd.lcd_puts(str(progress_list[i])+"%",11,1)
	
		i=i+1
		time.sleep(2)
