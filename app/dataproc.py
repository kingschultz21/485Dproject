# -*- encoding: utf-8 -*-
"""
Author: Connor Schultz
Date: 03/07/2020

Data processing Functions.
This program is not executed within the application.
It can be run locally to create the required shapefiles.

These shapefiles are then run through mapshaper-xl simply function
at a 0.1% simplification to reduce file size from 4.1Gb to 25Mb (wow!)
"""
# Python Modules
import os, logging

# Data Manipulation Modules
import numpy as np
import pandas as pd
import geopandas as gpd

import carto
import folium

# Project Directory
dir = os.getcwd()
# Global region names list 
region_names = ['centralcoast', 'skeena', 'nass']
#--------------------------------------------------------------- CENTRAL COAST REGION ----------------------------------------------------------------#
cc_header = [ ('chinook', 'cu_ck_cc.shp'), ('chum', 'zoi_spawning_cm_cc.shp'), ('coho', 'zoi_spawning_co_cc.shp'),
	        ('pink', 'zoi_spawning_pke_cc.shp'), ('pink', 'zoi_spawning_pko_cc.shp'), ('river_sockeye', 'zoi_spawning_ser_cc.shp') ] 

def format_region_attributes():
	'''
		Formats a region specific attribute table.
			-> returns: region_attr - dataframe corresponding to 'region_name'
	'''
	# Read in region population data obtained from psf.ca
	df = pd.read_csv(dir+'/app/static/assets/data/central_coast/'+'salmon_population.csv')
	# Subset for total run size, drop 'parameter' attribute
	df = df[df.parameter == 'Total run'].drop(['parameter'], axis=1)
	# Fix inconsistencies
	df.location = df.location.str.lower()
	df = df.rename(columns={'location': 'cu_name', 'datavalue': 'value'})											
	df.species = df.species.str.lower()														

	return df

def format_region_geometry(region_name, path, header):
	'''
		Formats several species specific shapefiles into one total geodataframe
			-> returns: region - geodataframe corresponding to 'region_name'
	'''
	print("Formatting region geometry: ",region_name)
	species_gdfs = []
	for tup in header:
		species = tup[0]
		fname = tup[1]
		# Read in species specific shapefile (not ideal) into geodataframe
		print("Reading: ",fname)
		gdf = gpd.read_file(path+species+'/'+fname)
		# Fix inconsistencies
		if species == 'chinook':
			continue
			gdf = gdf.rename(columns={'displaynam': 'cu_name', 'cu_species': 'species'})
		# Append to total species geodataframe list
		species_gdfs.append(gdf)
	# Merge (concatenate) species geodataframes, drop na values
	print("Merging species geodataframes")
	region = gpd.GeoDataFrame(pd.concat(species_gdfs, ignore_index=True), geometry='geometry').dropna(axis = 'columns')
	attrs = ['cuid', 'wtrshd_fid','regionname','cuname', 'shape_leng', 'shape_area', 'geometry']
	region = region[attrs]
	region = region.rename(columns={'cuname': 'cu_name'})
	region.cu_name = region.cu_name.str.lower()
	# Convert to WGS 84 for folium usage
	region.crs = 'EPSG:4326'

	return region


# --------------------- Output Functions ---------------------#
def create_shapefile():
	'''
		Joins a regions geometry geodataframe to a regions attribute dataframe.
		Writes a shapefile for each region.

		WARNING: this takes a looooooongggg time

		The shapefiles created within this function are then simplified using mapshaper
	'''
	path = dir+'/app/static/assets/data/central_coast/conservation_units/'
	# Format region geometry and attributes from shapefiles
	geom = format_region_geometry('centralcoast', path, cc_header)
	attr = format_region_attributes()
	# Attribute join with geometry based on conservation unit name (not ideal)
	print("Performing attribute merge")
	region = geom.merge(attr, on = 'cuname')		
	# Drop na values and redundant columns
	region = region.dropna()
	region = region.drop(['species_x'], axis=1)
	region = region.rename(columns={'species_y': 'species'})
	# Write joined geodataframe as ESRI shapefile
	fname = 'cc/cc_RAW.shp'
	print("Writing shapefile as ",fname)
	region.to_file(fname, driver='ESRI Shapefile')

	return region

def create_simple_shapefiles():
	region = gpd.read_file('cc/cc_simple.shp')
	print(region.species.value_counts())
	'''
		chum            39572
		coho            28708
		pink (even)     22112
		pink (odd)      20844
		lake sockeye     4872
		chinook          2490
	'''
	species = ['chum', 'coho', 'chinook', 'pink (even)', 'pink (odd)', 'lake sockeye']

	for fish in species:
		gdf = region[region.species == fish]
		print("Fish: ",fish,"Region: ","Central Coast")
		gdf.to_file('cc/'+fish+'/'+fish+".shp",driver='ESRI Shapefile')

attrs = format_region_attributes()
print(attrs.species.value_counts())
print(attrs.columns)
'''
path = r'app/static/assets/data/central_coast/conservation_units/'
geom = format_region_geometry('centralcoast',path,cc_header)
print(geom.columns)
geom = geom.drop_duplicates(subset=['wtrshd_fid'], keep='last')
geom = geom.dissolve(by='cu_name')
geom.to_file('test/wtrshds.shp',driver='ESRI Shapefile')
print(geom)
'''
esri_base = carto.init_map(location_start=[53.5, -124], zoom_start=6.25, tiles='Stamen Toner')
folium.GeoJson('test/test.geojson').add_to(esri_base)
folium.LayerControl().add_to(esri_base)

carto.to_html(esri_base, '/app/templates/pages', 'e_map.html')