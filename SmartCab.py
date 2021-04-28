#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 15:43:13 2021

@author: pi
"""

import os
import getpass
import csv
import time
import json
import datetime
import RPi.GPIO as GPIO
from cryptography.fernet import Fernet
from hx711 import HX711
from playsound import playsound



# Pin definitons
power_indicator_pin = 4
door_pin = 5
reminder_pin = 6
data_pin = 12
clock_pin = 13
tare_light_pin = 16
tare_button_pin = 17

# Pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(power_indicator_pin,GPIO.OUT)
GPIO.setup(door_pin,GPIO.IN)
GPIO.setup(reminder_pin,GPIO.OUT)
GPIO.setup(tare_light_pin,GPIO.OUT)
GPIO.setup(tare_button_pin,GPIO.IN)

# Turn LEDs on or off
GPIO.output(power_indicator_pin,GPIO.HIGH)
GPIO.output(reminder_pin,GPIO.LOW)
GPIO.output(tare_light_pin,GPIO.LOW)

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
            med_time = input("Please input the hour that you are supposed to take your medication, in 2-digit 24-hour format: ")
            med_time = int(med_time)
            if len(str(med_time)) != 2:
                print("Please remember to add a 0 for single-digit times")
            elif med_time >= 0 and med_time <= 24:
                med_times = [med_time]
                schedule_specified = True
            else:
                print("Please enter a number between 0 and 24")
        elif schedule == 2:
            med_time1 = input("Please input the first hour that you are supposed to take your medication, in 2-digit 24-hour format: ")
            med_time1 = int(med_time1)
            med_time2 = input("Please input the second hour that you are supposed to take your medication, in 2-digit 24-hour format: ")
            med_time2 = int(med_time2)
            if len(str(med_time1)) != 2 or len(str(med_time2)) != 2:
                print("Please remember to add a 0 for single-digit times")
            elif med_time1 >= 0 and med_time1 <= 24 and med_time2 >= 0 and med_time2 <= 24:
                med_times = [med_time1,med_time2]
                schedule_specified = True
            else:
                print("Please enter a number between 0 and 24")
        else:
            print("Please enter a number between 0 and 2")
    sensor_tared = False
    while sensor_tared == False:
        playsound("audio_files/place_cap.wav")
        cap_on = input("Please place the cap of the medication bottle in the cabinet, if applicable, and enter \"done\" when you have done that: ")
        if cap_on == "done":
            hx.tare()
            print(hx.get_weight(11))
            sensor_tared = True
    pills_weighed = False
    while pills_weighed == False:
        playsound("audio_files/place_doses.wav")
        pill_number = input("Please place 1 to 10 doses of your medication on the scale (10 would be best), and enter the number of doses you have placed: ")
        pill_number = int(pill_number)
        if type(pill_number) == int:
            total_weight = hx.get_weight(21)
            medication_weight = total_weight / pill_number
            pills_weighed = True
    bottle_weighed = False
    GPIO.output(tare_light_pin,GPIO.HIGH)
    print("Please return the medication into its bottle and clear everything from the cabinet. Please press the tare button when finished.")
    playsound("audio_files/return_med.wav")
    while bottle_weighed == False:
        if GPIO.input(tare_button_pin) == True:
            GPIO.output(tare_light_pin,GPIO.LOW)
            hx.tare()
            print("Please place the entire medication bottle in the cabinet, and close the door.")
            playsound("audio_files/place_in_cab.wav")
            door_open = True
            while door_open == True:
                if GPIO.input(door_pin) == True:
                    door_open = False
            time.sleep(5)
            current_time = datetime.datetime.now()
            current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            medication_history = [current_time, hx.get_weight(11)]
            with open(f"Users/{name}/medication_history.csv",'a') as med_hist:
                writer = csv.writer(med_hist)
                writer.writerow(medication_history)
            bottle_weighed = True
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
    playsound("audio_files/setup_complete.wav")
else:
    name = os.listdir("Users")[0]
    medication_weight = open(f"Users/{name}/medication_weight.txt","rb").read()
    medication_weight = float(fn.decrypt(medication_weight).decode("utf-8"))
    med_times = open(f"Users/{name}/medication_schedule.txt","rb").read()
    med_times = fn.decrypt(med_times).decode("utf-8")

# Try to decode what time(s) the medication should be taken
med_times = json.loads(med_times)
if len(med_times) == 1:
    med_time1 = med_times[0]
    med_time1 = f"{med_time1}00"
    med_time1 = int(med_time1)
else:
    med_time1 = "None"
if len(med_times) == 2:
    med_time1 = med_times[1]
    med_time2 = f"{med_time2}00"
    med_time2 = int(med_time2)
    print(med_time2)
else:
    med_time2 = "None"

# SmartCab program
print("PillSafe Cab Program Running")
reminder = True
try:
    while 1:
        
        # Check to see if reminder needs to be set
        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%H%M")
        if current_time == med_time1 or current_time == med_time2:
            reminder = True
        
        if reminder == True:
            GPIO.output(reminder_pin,GPIO.HIGH)
        
        # Checks to see if door is open
        if GPIO.input(door_pin) == False:
            door_open = True
        else:
            door_open = False
        
        # Reminds patient to tare cabinet each time
        if door_open == True:
            tared = False
            GPIO.output(tare_light_pin,GPIO.HIGH)
            print("Please clear everything from the cabinet, and press the tare button.")
            playsound("audio_files/daily_tare.wav")
            while tared == False and door_open == True:
                if GPIO.input(tare_button_pin) == True:
                    print("button pressed")
                    GPIO.output(tare_light_pin,GPIO.LOW)
                    hx.tare()
                    
                    # Weighs medication bottle and records weight
                    print("Please take your medication, return the bottle to the cabinet, and close the door.")
                    playsound("audio_files/take_med.wav")
                    while door_open == True:
                        if GPIO.input(door_pin) == True:
                            door_open = False
                    time.sleep(3)
                    current_time = datetime.datetime.now()
                    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                    current_bottle_weight = hx.get_weight(21)
                    medication_history = [current_time,current_bottle_weight]
                    with open(f"Users/{name}/medication_history.csv",'a') as med_hist:
                        writer = csv.writer(med_hist)
                        writer.writerow(medication_history)
                    tared = True
                    
                    # Calculates the number of doses taken
                    with open(f"Users/{name}/medication_history.csv") as csv_file:
                        csv_reader = csv.reader(csv_file)
                        lines_total = len(list(csv_reader))
                    with open(f"Users/{name}/medication_history.csv") as csv_file:
                        csv_reader = csv.reader(csv_file)
                        line_count = 1
                        for row in csv_reader:
                            if line_count == lines_total-1:
                                last_bottle_weight = float(row[1])
                            line_count += 1
                    doses = (last_bottle_weight-current_bottle_weight) / medication_weight
                    doses = round(doses)
                    
                    # See if it was time to take medication
                    if reminder == False:
                        print("Please make sure to take your medication at the specified time")
                        playsound("audio_files/not_time.wav")
                    
                    # Resets reminder light
                    if doses >= 1:
                        reminder = False
                        GPIO.output(reminder_pin,GPIO.LOW)
                    
                    # Check the number of doses taken
                    if doses == 0:
                        print("Please make sure you take your medication!")
                        playsound("audio_files/take_your_pills.wav")
                    if doses > 1:
                        print("Please make sure to take the correct dose of your medication.")
                        playsound("audio_files/correct_dose.wav")
                
                # Alternative exit in case user changes mind and closes door
                if GPIO.input(door_pin) == True:
                    GPIO.output(tare_light_pin,GPIO.LOW)
                    door_open = False
            
            
        
        # Time delay to save CPU cycles
        time.sleep(0.5)

# Exit code
except KeyboardInterrupt:
    GPIO.cleanup()
