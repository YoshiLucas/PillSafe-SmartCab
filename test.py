#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 20:49:38 2021

@author: pi
"""
"""
# LED test
import RPi.GPIO as GPIO
light_pin = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(light_pin,GPIO.OUT)
try:
    while 1:
        GPIO.output(light_pin,GPIO.HIGH)
except KeyboardInterrupt:
    GPIO.cleanup()
"""
"""
# Button test
import RPi.GPIO as GPIO
import time
tare_button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(tare_button_pin,GPIO.IN)
try:
    while 1:
        print(GPIO.input(tare_button_pin))
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
"""
"""
# CSV test
import csv
name = "Yoshi"
with open(f"Users/{name}/medication_history.csv") as csv_file:
    csv_reader = csv.reader(csv_file)
    lines_total = len(list(csv_reader))
with open(f"Users/{name}/medication_history.csv") as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 1
    for row in csv_reader:
        if line_count == lines_total:
            print(row[1])
        line_count += 1
"""
"""
# Demonstration of various errors that could come up
print("PillSafe Cab Program Running")
print("Please clear everything from the cabinet, and press the tare button.")
print("Please place take your medication, return the bottle to the cabinet, and close the door.")
print("Please make sure to take your medication at the specified time")
print("Please make sure you take your medication!")
print("Please make sure to take the correct dose of your medication.")
"""

from hx711 import HX711
import time
data_pin = 12
clock_pin = 13
hx = HX711(data_pin, clock_pin)
hx.set_reading_format("MSB", "MSB")
hx.tare()
while 1:
    print(hx.get_weight(9))
#    time.sleep(0.5)

"""
# 
from playsound import playsound
playsound('CantinaBand60.wav')
"""


