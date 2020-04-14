# -*- encoding: utf-8 -*-
"""
Author: Connor Schultz
Date: 03/07/2020

Mapping Functions used to create the GISalmon
Interactive Web-Map
"""
# Python Modules
import os, logging 

# Flask Modules
from flask import render_template

# Mapping Modules
import folium

# --------------------- Initialization Functions ---------------------#

def init_map(location_start, zoom_start, tiles):
	'''
		Initialize a blank map from parameters
			-> returns: map - folium map object
	'''
	map = folium.Map(location=location_start, 
					 zoom_start=zoom_start, 
					 tiles=tiles)
	return map

def init_google_map(location_start, zoom_start):
	'''
		Initialize a blank map with Google Earth Imagery Basemap
			-> returns: map - folium map object
	'''
	GoogleImagery = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'
	GoogleAttr = 'Google'
	map = folium.Map(location=location_start, 
					 zoom_start=zoom_start, 
					 tiles=GoogleImagery,
					 attr=GoogleAttr)
	return map

def init_esri_map(location_start, zoom_start):
	'''
		Initialize a blank map with ESRI World Imagery Basemap
			-> returns: map - folium map object
	'''
	EsriImagery = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
	EsriAttr = "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"
	map = folium.Map(location=location_start, 
					 zoom_start=zoom_start, 
					 tiles=EsriImagery,
					 attr=EsriAttr)
	return map

# --------------------- Output Functions ---------------------#

def to_html(map, path, fname):
	'''
		Converts a map to html and saves in the given path location
	'''
	cwd = os.getcwd()

	map.save(fname)
	os.replace(cwd+'/'+fname, cwd+path+'/'+fname)