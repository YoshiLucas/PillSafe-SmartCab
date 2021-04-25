#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 23:13:53 2021

@author: pi
"""

from flask import Blueprint
from . import db



auth = Blueprint("auth",__name__)

@auth.route("/login")
def login():
    return "Login"

@auth.route("/logout")
def logout():
    return "Logout"