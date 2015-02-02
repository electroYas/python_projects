#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x20 for a 16 chars and 2 line display
int col,row;
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

void setup()
{
  Serial.begin(9600);
  lcd.init();                     
  lcd.backlight();  
  lcd.print("Arduino Uno");
  delay(1000);
  col=0;
  row=0;
  lcd.clear();
  
}

void loop()
{
  if (stringComplete) {
   lcd.clear();
   lcd.setCursor(0,0);
   for(int i=0;i<inputString.length();i++){
     if(inputString[i]=='\n') continue;
     lcd.print(inputString[i]);
     col++;
     delay(80);
 
     if(col>15 && row==0){
       lcd.setCursor(0,1);
       row=1;
       col=0;   
     } 
    
     if(col>15 && row==1){
       delay(500);
       lcd.clear();
       lcd.setCursor(0,0);
       row=0;
       col=0;
     } 
    // clear the string:
    
   }
   
   inputString = "";
   stringComplete = false;
  }
 
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read(); 
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
}
