# -*- encoding: utf-8 -*-
"""
Author: Connor Schultz
Date: 03/07/2020

Basic routing program using Flask.
"""
# Python Modules
import os, logging 

# App Modules
from app import app
from app import carto

# Flask Modules
from flask import render_template

# Mapping Modules
import folium


# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):
	e_map = carto.init_esri_map(location_start=[53.5, -124], zoom_start=6.25)
	carto.to_html(e_map, '/app/templates/pages', 'e_map.html')

	g_map = carto.init_google_map(location_start=[53.5, -124], zoom_start=6.25)
	carto.to_html(g_map, '/app/templates/pages', 'g_map.html')

	try:
		# try to match the pages defined in -> pages/<input file>
		return render_template( 'pages/'+path )

	except:
		# return 404 error page
		return render_template( 'pages/error-404.html' )