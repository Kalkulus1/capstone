#Libraries
import os
import threading
import urllib2
import RPi.GPIO as GPIO
import time
import lcddriver
#from time import *

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
lcd = lcddriver.lcd()
lcd.lcd_clear()

def lcd_welcome():
    lcd.lcd_display_string("      Welcome!", 1)
    lcd.lcd_display_string("Wait For 30 Seconds!", 3)

lcd_welcome()
time.sleep(5)
lcd.lcd_clear()
lcd.lcd_display_string(" Starting...",2)
time.sleep(5)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(1)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance
def send_data_to_server():
    dist  = distance()
    flowr = dist/5
    threading.Timer(600,send_data_to_server).start()
    print("Sensing...")
    print ("Measured Distance = %.1f cm" % dist)
    #print ("Measured Flow  = %.1f cm" % flowr)
    level = str(dist)
    urllib2.urlopen("http://teknoprojects.tech/add_data.php?fuel_level="+level).read()


if __name__ == '__main__':
    try:
        while True:
            send_data_to_server()
            lcd.lcd_clear()
            lcd.lcd_display_string("Sensing...",1)
            lcd.lcd_display_string("Capturing Distance",2)
            time.sleep(5)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        lcd.lcd_clear()
        lcd.lcd_display_string("Sensor stopped.",1)
        time.sleep(5)
        GPIO.cleanup()
