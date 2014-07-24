import smbus
import time

LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80
# flags for display entry mode
LCD_ENTRYRIGHT =0x00
LCD_ENTRYLEFT =0x02
LCD_ENTRYSHIFTINCREMENT =0x01
LCD_ENTRYSHIFTDECREMENT =0x00
# flags for display on/off control
LCD_DISPLAYON =0x04
LCD_DISPLAYOFF= 0x00
LCD_CURSORON =0x02
LCD_CURSOROFF =0x00
LCD_BLINKON= 0x01
LCD_BLINKOFF =0x00
#flags for display/cursor shift
LCD_DISPLAYMOVE =0x08
LCD_CURSORMOVE =0x00
LCD_MOVERIGHT =0x04
LCD_MOVELEFT =0x00
# flags for function set
LCD_8BITMODE =0x10
LCD_4BITMODE =0x00
LCD_2LINE =0x08
LCD_1LINE =0x00
LCD_5x10DOTS =0x04
LCD_5x8DOTS =0x00

#displayfunction=0

#Have to change according to the LCD and I2C device
LCD_BACKLIGHT =0x08	#changed
LCD_NOBACKLIGHT =0x00	#changed
En = 0b00000100  #// Enable bit	\\changed
Rw = 0b00000010  #// Read/Write bit	\\changed
Rs = 0b00000001  #// Register select bit\\changed

displaycontrol=0
displaymode=0
backlightval =0 

class I2c_device:
	def __init__(self, addr, port):
		self.addr = addr
		self.bus = smbus.SMBus(port)
 
	def write(self, byte):
		self.bus.write_byte(self.addr, byte)
 
	def read(self):
		return self.bus.read_byte(self.addr)
 
	def read_nbytes_data(self, data, n): 
		return self.bus.read_i2c_block_data(self.addr, data, n)
 
class Lcd:

	
	def __init__(self):
		self.lcd = I2c_device(0x27,1)
		time.sleep(0.050)
		self.begin()
		
	def display(self):
		global displaycontrol
		displaycontrol |= LCD_DISPLAYON;
		self.command(LCD_DISPLAYCONTROL | displaycontrol);
	
	def clear(self):
		self.command(LCD_CLEARDISPLAY)
		time.sleep(0.5)

	def begin(self): 
		
		global displaycontrol
		global displaymode
		
		self.expanderWrite(backlightval)
		time.sleep(1)
		self.write4bits(0x03<<4)#;//changed
		time.sleep(0.0041)
		self.write4bits(0x03<<4)#;//changed
		time.sleep(0.0041)
		self.write4bits(0x03<<4)#; //changed
		time.sleep(0.150)
		self.write4bits(0x02<<4)#; //changed
		displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF;
		self.display();
		self.clear();
		displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT;
		self.command(LCD_ENTRYMODESET | displaymode);
		self.home();

	def noBacklight(self):
		global backlightval
		backlightval=LCD_NOBACKLIGHT
		self.expanderWrite(0)


	def backlight(self):
		global backlightval
		
		backlightval=LCD_BACKLIGHT
		self.expanderWrite(0)

#/*********** mid level commands, for sending data/cmds */

	def command(self,value):
		self.send(value, 0)
	
	def write(self,value):
		self.send(value, Rs)
		return 0

#/************ low level data pushing commands **********/

#// write either command or data
	def send(self,value,mode):
		highnib=value & 0xF0 #;//changed
		lownib=value << 4 #;//changed
		self.write4bits((highnib)|mode)
		self.write4bits((lownib)|mode)

	def write4bits(self,value):
		self.expanderWrite(value)
		self.pulseEnable(value)

	def expanderWrite(self,_data):    
		self.lcd.write(_data | backlightval)                                 

	def pulseEnable(self,_data):
		self.expanderWrite(_data | En)
		time.sleep(0.000001)	
		self.expanderWrite(_data & ~En)
		time.sleep(0.000050)		


	def home(self):
		self.command(LCD_RETURNHOME)
		time.sleep(0.5)

	def lcd_putc(self, char):
		self.write(ord(char))
 
	def lcd_puts(self, string, col, line):
		self.setCursor(col,line)
		for char in string:
			self.lcd_putc(char)
		
	def setCursor(self,col, row):
		row_offsets = [0x00,0x40,0x14,0x54]	
		self.command(LCD_SETDDRAMADDR | (col + row_offsets[row]))


