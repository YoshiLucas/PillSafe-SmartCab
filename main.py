#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 23:12:52 2021

@author: pi
"""

from flask import Blueprint
from . import db



main = Blueprint("main",__name__)

@auth.route("/")
def index():
    return "Index"

@auth.route("/profile")
def profile():
    return "Profile"