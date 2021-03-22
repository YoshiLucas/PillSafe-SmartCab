#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 15:43:13 2021

@author: pi
"""

from flask import Flask, url_for
from markupsafe import escape



app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % escape(username)

with app.test_request_context():
    print(url_for('index'))