import lcddriver
from time import *
import time 
lcd = lcddriver.lcd()
lcd.lcd_clear()
 
lcd.lcd_display_string("DO NOT TOUCH PLEASE", 1)
lcd.lcd_display_string("DO NOT TOUCH PLEASE", 3)
lcd.lcd_display_string("DO NOT TOUCH PLEASE", 2)
lcd.lcd_display_string("DO NOT TOUCH PLEASE", 4)
sleep(5)
lcd.lcd_clear()
lcd.lcd_display_string("Hello Ghana",1)


