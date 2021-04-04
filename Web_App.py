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
from threading import Thread
from flask import Flask,flash,render_template,request,url_for
from markupsafe import escape



# Pin definitons
power_indicator_pin = 4
door_pin = 5
reminder_pin = 6

# Pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(power_indicator_pin,GPIO.OUT)
GPIO.setup(door_pin,GPIO.IN)
GPIO.setup(reminder_pin,GPIO.OUT)



# Generates a key for encryption and decryption if it doesn't already exist
if os.path.exists("key.key") == False:
    key = Fernet.generate_key()
    with open("key.key","wb") as key_file:
        key_file.write(key)
else:
    key = open("key.key","rb").read()
fn = Fernet(key)

# Generate user data if no users are present
if os.path.exists("Users/password.txt")==False or os.path.exists("Users/medication.txt")==False:
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
        if schedule = 




"""

# Set up web application
app = Flask(__name__)

# Home page
@app.route("/",methods=["GET"])
def home():
    
    try:
        user = os.listdir('Users')[0]
        return render_template("home.html",user)
    except IndexError:
        username = request.args.get("username", "")

        os.mkdir(f"User/{username}")

        return (""
                <form action = "" method = "get">
                    <input type = "text" name = "username">
                </form>
                ""
                + username
                )

"""
"""
@app.route('/<celsius>')
def fahrenheit_from(celsius):
    try:
        fahrenheit = float(celsius) * 9/5 + 32
        fahrenheit = round(fahrenheit,3)
        return str(fahrenheit)
    except ValueError:
        return "invalid input"

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % escape(username)
"""
"""

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug=True)
"""
GPIO.cleanup()
