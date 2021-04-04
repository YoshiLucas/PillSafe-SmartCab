#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 15:43:13 2021

@author: pi
"""

import os
import getpass
import time
import RPi.GPIO as GPIO
from cryptography.fernet import Fernet
from hx711 import HX711



# Pin definitons
power_indicator_pin = 4
door_pin = 5
reminder_pin = 6
data_pin = 12
clock_pin = 13

# Pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(power_indicator_pin,GPIO.OUT)
GPIO.setup(door_pin,GPIO.IN)
GPIO.setup(reminder_pin,GPIO.OUT)

# Indicator light for power
GPIO.output(power_indicator_pin,GPIO.HIGH)

# HX711 setup
hx = HX711(data_pin, clock_pin)
hx.set_reading_format("MSB", "MSB")



# Generates a key for encryption and decryption if it doesn't already exist
if os.path.exists("key.key") == False:
    key = Fernet.generate_key()
    with open("key.key","wb") as key_file:
        key_file.write(key)
else:
    key = open("key.key","rb").read()
fn = Fernet(key)

# Generate user data if no users are present
if len(os.listdir("Users")) == 0:
    print("Welcome, new user!")
    name = input("Please enter your name: ")
    password_match = False
    while password_match == False:
        password1 = getpass.getpass("Please create a password: ")
        password2 = getpass.getpass("Please reenter your password ")
        if password1 == password2:
            password_match = True
        else:
            print("Passwords do not match!")
    medication = input("Please enter the name of your medication: ")
    schedule_specified = False
    while schedule_specified == False:
        schedule = input("How often are you supposed to take your medication daily? Enter 1 for \"once a day\", 2 for \"twice a day\", and 0 for \"as needed\": ")
        schedule = int(schedule)
        if schedule == 0:
            med_times = []
            schedule_specified = True
        elif schedule == 1:
            med_time = input("Please input the hour that you are supposed to take your medication, in 24-hour format: ")
            med_time = int(med_time)
            if med_time >= 0 and med_time <= 24:
                med_times = [med_time]
                schedule_specified = True
            else:
                print("Please enter a number between 0 and 24")
        elif schedule == 2:
            med_time1 = input("Please input the first hour that you are supposed to take your medication, in 24-hour format: ")
            med_time1 = int(med_time1)
            med_time2 = input("Please input the second hour that you are supposed to take your medication, in 24-hour format: ")
            med_time2 = int(med_time2)
            if med_time1 >= 0 and med_time1 <= 24 and med_time2 >= 0 and med_time2 <= 24:
                med_times = [med_time1,med_time2]
                schedule_specified = True
            else:
                print("Please enter a number between 0 and 24")
        else:
            print("Please enter a number between 0 and 2")
    sensor_tared = False
    while sensor_tared == False:
        cap_on = input("Please place the cap of the medication bottle in the cabinet, if applicable, and enter \"done\" when you have done that: ")
        if cap_on == "done":
            hx.tare()
            print(hx.get_weight(11))
            sensor_tared = True
    pills_weighed = False
    while pills_weighed == False:
        pill_number = input("Please place 1 to 10 doses of your medication on the scale (10 would be best), and enter the number of doses you have placed: ")
        pill_number = int(pill_number)
        if type(pill_number) == int:
            total_weight = hx.get_weight(21)
            medication_weight = total_weight / pill_number
            pills_weighed = True
    if os.path.exists(f"Users/{name}")==False:
        os.mkdir(f"Users/{name}")
    with open(f"Users/{name}/password.txt","wb") as password_file:
        password_file.write(fn.encrypt(str(password1).encode()))
    with open(f"Users/{name}/medication_name.txt","wb") as medication_name_file:
        medication_name_file.write(fn.encrypt(str(medication).encode()))
    with open(f"Users/{name}/medication_schedule.txt","wb") as medication_schedule_file:
        medication_schedule_file.write(fn.encrypt(str(med_times).encode()))
    with open(f"Users/{name}/medication_weight.txt","wb") as medication_weight_file:
        medication_weight_file.write(fn.encrypt(str(medication_weight).encode()))
    print("Setup is complete! You can now take your medication as prescribed.")
else:
    user = os.listdir("Users")[0]
    medication_weight = open(f"Users/{user}/medication_weight.txt","rb").read()
    medication_weight = float(fn.decrypt(medication_weight).decode("utf-8"))
    print(medication_weight)

# SmartCab program
print("PillSafe Cab Program Running")
try:
    while 1:
        
        # Checks to see if door is open
        if GPIO.input(door_pin) == True:
            door_open = True
        else:
            door_open = False
        
        # Starts measuring weight to see when to tare
        if door_open == True:
            hx.tare()
            tared = False
            while tared == False:
                tared 
            
            time.sleep(1)
            

        
        
        
        GPIO.output(reminder_pin,GPIO.HIGH)
        """
        # Reminder light for medication
        if medication_taken == False:
            GPIO.output(reminder_pin,GPIO.HIGH)
        if medication_taken == True:
            GPIO.output(reminder_pin,GPIO.LOW)"""
# Exit code
except KeyboardInterrupt:
    GPIO.cleanup()
