#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 15:43:13 2021

@author: pi
"""

import os
import getpass
import time
from cryptography.fernet import Fernet
from flask import Flask,flash,render_template,request,url_for
from markupsafe import escape



# Generates a key for encryption and decryption if it doesn't already exist
if os.path.exists("key.key") == True:
    key = open("key.key","rb").read()
    fn = Fernet(key)
else:
    print("Error! User data missing! Please generate it using the main SmartCab program.")

# Set up web application
app = Flask(__name__)

"""
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

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug=True)

