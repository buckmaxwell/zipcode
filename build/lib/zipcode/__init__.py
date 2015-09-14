__author__ = 'Max Buck'
__email__ = 'maxbuckdeveloper@gmail.com'
__license__ = 'MIT'
__package__ = 'zipcode'
__version__ = '1.7.0'


import sqlite3 as db
import os
from haversine import haversine
import math

db_filename = 'zipcode.db'
directory = os.path.dirname(os.path.abspath(__file__))
zipcodedb_location = os.path.join(directory, db_filename)
conn = db.connect(zipcodedb_location)


cur = conn.cursor()

ZIP_CODE = 0
ZIP_CODE_TYPE = 1
CITY= 2
STATE = 3
LOCATION_TYPE = 4
LAT = 5
LONG = 6
XAXIS = 7
YAXIS = 8
ZAXIS = 9
WORLD_REGION = 10
COUNTRY = 11
LOCATION_TEXT = 12
LOCATION = 13
DECOMMISIONED = 14
TAX_RETURNS_FILED = 15
ESTIMATED_POPULATION = 16
TOTAL_WAGES = 17
NOTES = 18

class Zip(object):
	"""Holds a zip code"""
	def __init__(self, zip_tuple):
		self.zip = zip_tuple[ZIP_CODE]
		self.zip_type = zip_tuple[ZIP_CODE_TYPE]
		self.city = zip_tuple[CITY]
		self.state = zip_tuple[STATE]
		self.location_type = zip_tuple[LOCATION_TYPE]
		self.lat = zip_tuple[LAT]
		self.lon = zip_tuple[LONG]
		self.xaxis = zip_tuple[XAXIS]
		self.yaxis = zip_tuple[YAXIS]
		self.zaxis = zip_tuple[ZAXIS]
		self.world_region = zip_tuple[WORLD_REGION]
		self.country = zip_tuple[WORLD_REGION]
		self.location_text = zip_tuple[LOCATION_TEXT]
		self.location = zip_tuple[LOCATION]
		self.decommisioned = zip_tuple[DECOMMISIONED]
		self.tax_returns_filed = zip_tuple[TAX_RETURNS_FILED]
		self.population = zip_tuple[ESTIMATED_POPULATION]
		self.wages = zip_tuple[TOTAL_WAGES]
		self.notes = zip_tuple[NOTES]

	def __repr__(self):
		return '<Zip: {zip}>'.format(zip=self.zip)

	def to_dict(self):
		return vars(self)

def make_zip_list(list_of_zip_tuples):
	zip_list = list()
	for zip_tuple in list_of_zip_tuples:
		z = Zip(zip_tuple)
		zip_list.append(z)
	return zip_list


def validate(zipcode):
	"""Checks for a valid zipcode and throws error if not valid"""
	if not isinstance(zipcode, str):
		raise TypeError('zipcode should be a string')
	int(zipcode) # This could throw an error if zip is not made of numbers
	return True

def islike(zipcode):
	validate(zipcode)
	cur.execute('SELECT * FROM ZIPS WHERE ZIP_CODE LIKE ?', ['{zipcode}%'.format(zipcode=str(zipcode))])
	return make_zip_list(cur.fetchall())

def isequal(zipcode):
	validate(zipcode)
	cur.execute('SELECT * FROM ZIPS WHERE ZIP_CODE == ?', [str(zipcode)])
	row = cur.fetchone()
	if row:
		return Zip(row)
	else:
		return None

def isinradius(point, distance):
	zips_in_radius = list()
	
	if not isinstance(point, tuple):
		raise TypeError('point should be a tuple of floats')
	for f in point:
		if not isinstance(f, float):
			raise TypeError('lat and lon must be of type float')

	dist_btwn_lat_deg = 69.172
	dist_btwn_lon_deg = math.cos(point[0]) * 69.172
	lat_degr_rad = float(distance)/dist_btwn_lat_deg
	lon_degr_rad = float(distance)/dist_btwn_lon_deg

	latmin = point[0] - lat_degr_rad
	latmax = point[0] + lat_degr_rad
	lonmin = point[1] - lon_degr_rad
	lonmax = point[1] + lon_degr_rad

	if latmin > latmax:
		latmin, latmax = latmax, latmin
	if lonmin > lonmax:
		lonmin, lonmax = lonmax, lonmin

	stmt = ('SELECT * FROM ZIPS WHERE LONG > {lonmin} AND LONG < {lonmax}\
	 AND LAT > {latmin} AND LAT < {latmax}')
	cur.execute(stmt.format(lonmin=lonmin, lonmax=lonmax, latmin=latmin, latmax=latmax))
	results = cur.fetchall()
	
	for row in results:
		if haversine(point, (row[LAT], row[LONG])) <= distance:
			zips_in_radius.append(Zip(row))
	return zips_in_radius



















