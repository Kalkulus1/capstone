#Libraries
from Crypto.PublicKey import RSA
import os
import threading
import urllib2 as r
import RPi.GPIO as GPIO
import time
import lcddriver
import math
import mysql.connector

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
    lcd.lcd_display_string("Wait For 10 Seconds!", 3)
    time.sleep(5)
    lcd.lcd_clear()
    lcd.lcd_display_string(" Starting...",2)
    time.sleep(5)
lcd_welcome()


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

    return distance, TimeElapsed

###Encryption Algorithm###
key = RSA.generate(4096)
publicKey = key.publickey()
def encryption(plain):
    ciphertext = publicKey.encrypt(plain, 0)[0]
    encrypted = ciphertext.encode("hex")
    return ciphertext, encrypted


###remote sql connection###
mydb = mysql.connector.connect(
  host="sql122.main-hosting.eu",
  user="u522087490_kalkulus",
  passwd="kalkulus32",
  database="u522087490_project"
)
mycursor = mydb.cursor()


def send_data_to_server():
    total_distance = 300
    radius = 100
    dist, time  = distance()
    flowrate = dist/time
    volume_used = math.pi * (radius**2) * dist
    volume_remained = math.pi * (radius**2) * (total_distance - dist)
    volume_flowrate = volume_used/time
    threading.Timer(600,send_data_to_server).start()
    print "Sensing..."
    print "Measured Distance = %.1f cm" % dist
    #print ("Measured Flow  = %.1f cm" % flowr)
    level_used = str(dist)
    level_remained = str(total_distance - dist)
    clevel_u,elevel_u = encryption(level_used)
    clevel_r,elevel_r = encryption(level_remained)
    date_now = time.strftime("%Y-%m-%d")
    time_now = time.strftime("%H:%M:%S")
    sql_query = "INSERT INTO Users (date_now, time_now, clevelu, elevelu, clevelr, elevelr) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (date_now, time_now, clevel_u, elevel_u, clevel_r, elevel_r)
    mycursor.execute(sql_query, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    #r.urlopen("http://teknoprojects.tech/add_data.php?fuel_level="+elevel_u).read()


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
        print "Measurement stopped by User"
        lcd.lcd_clear()
        lcd.lcd_display_string("Sensor stopped.",1)
        time.sleep(5)
        GPIO.cleanup()


