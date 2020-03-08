# -*- encoding: utf-8 -*-
"""
Author: Connor Schultz
Date: 03/07/2020

Mapping Functions used to create the GISalmon
interactive web-map
"""
# Python Modules
import os, logging 

# Flask Modules
from flask import render_template

# Mapping Modules
import folium

class Map