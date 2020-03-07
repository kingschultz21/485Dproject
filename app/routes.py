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

# Flask Modules
from flask import render_template

# Project Mapping Modules
import folium

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):
	# Link to Esri World Imagery service plus attribution
	EsriImagery = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
	EsriAttribution = "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"

	cwd = os.getcwd()

	# GOOGLE MAP
	m = folium.Map(location=[53.5, -124], zoom_start=6.25, tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',attr = 'Google')
	m.save('map.html')
	# Sad fix to move html files from one directory to another as saving outside the cwd does
	# not appear to be possible in folium
	os.replace(cwd+'/map.html',cwd+'/app/templates/pages/map.html')
	print(cwd)
	# ESRI MAP
	m = folium.Map(location=[53.5, -124], zoom_start=6.25, tiles = EsriImagery,attr = EsriAttribution)
	m.save('map2.html')
	os.replace(cwd+'/map2.html',cwd+'/app/templates/pages/map2.html')
	print(path)
	try:
		# try to match the pages defined in -> pages/<input file>
		return render_template( 'pages/'+path )

	except:
		# return 404 error page
		return render_template( 'pages/error-404.html' )