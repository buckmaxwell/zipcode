__author__ = 'Max Buck'
__email__ = 'maxbuckdeveloper@gmail.com'
__license__ = 'MIT'
__package__ = 'zipcode'
__version__ = '2.0.0'


import sqlite3 as db
import os
from haversine import haversine
import math

_db_filename = 'zipcode.db'
_directory = os.path.dirname(os.path.abspath(__file__))
_zipcodedb_location = os.path.join(_directory, _db_filename)
_conn = db.connect(_zipcodedb_location)


_cur = _conn.cursor()

# positions
_ZIP_CODE = 0
_ZIP_CODE_TYPE = 1
_CITY= 2
_STATE = 3
_LOCATION_TYPE = 4
_LAT = 5
_LONG = 6
_XAXIS = 7
_YAXIS = 8
_ZAXIS = 9
_WORLD_REGION = 10
_COUNTRY = 11
_LOCATION_TEXT = 12
_LOCATION = 13
_DECOMMISIONED = 14
_TAX_RETURNS_FILED = 15
_ESTIMATED_POPULATION = 16
_TOTAL_WAGES = 17
_NOTES = 18

class Zip(object):
	"""The zip code object."""
	def __init__(self, zip_tuple):
		self.zip = zip_tuple[_ZIP_CODE]
		"""The 5 digit zip code"""
		self.zip_type = zip_tuple[_ZIP_CODE_TYPE]
		"""The type of zip code according to USPS: 'UNIQUE', 'PO BOX', or 'STANDARD'"""
		self.city = zip_tuple[_CITY]
		"""The primary city associated with the zip code according to USPS"""
		self.state = zip_tuple[_STATE]
		"""The state associated with the zip code according to USPS"""
		self._location_type = zip_tuple[_LOCATION_TYPE] 
		# This value will always be 'Primary'. Secondary and 'Not Acceptable' placenames have been removed.
		self.lat = zip_tuple[_LAT]
		"""The latitude associated with the zipcode according to the National Weather Service.  This can be empty when there is no NWS Data"""
		self.lon = zip_tuple[_LONG]
		"""The longitude associated with the zipcode according to the National Weather Service. This can be empty when there is no NWS Data"""
		self._xaxis = zip_tuple[_XAXIS]
		self._yaxis = zip_tuple[_YAXIS]
		self._zaxis = zip_tuple[_ZAXIS]
		self._world_region = zip_tuple[_WORLD_REGION]
		# This value will always be NA for North America
		self._country = zip_tuple[_WORLD_REGION]
		# This value will always be US for United States -- This includes Embassy's, Military Bases, and Territories
		self.location_text = zip_tuple[_LOCATION_TEXT]
		"""The city with its state or territory. Example:  'Cleveland, OH' or 'Anasco, PR'"""
		self.location = zip_tuple[_LOCATION]
		"""A string formatted as WORLD_REGION-COUNTRY-STATE-CITY. Example: 'NA-US-PR-ANASCO'"""
		self.decommisioned = zip_tuple[_DECOMMISIONED]
		"""A boolean value that reveals if a zipcode is still in use"""
		self.tax_returns_filed = zip_tuple[_TAX_RETURNS_FILED]
		"""Number of tax returns filed for the zip code in 2008 according to the IRS"""
		self.population = zip_tuple[_ESTIMATED_POPULATION]
		"""Estimated population in 2008 according to the IRS"""
		self.wages = zip_tuple[_TOTAL_WAGES]
		"""Total wages according in 2008 according to the IRS"""
		self._notes = zip_tuple[_NOTES]
		# Not empty when there is no NWS data.

	def __repr__(self):
		return '<Zip: {zip}>'.format(zip=self.zip)

	def to_dict(self):
		vars_self = vars(self)
		bad_key_list = [x for x in vars_self.keys() if x[0] == '_']
		for key in vars_self.keys():
			if key in bad_key_list:
				del vars_self[key]
		return vars_self

def _make_zip_list(list_of_zip_tuples):
	zip_list = list()
	for zip_tuple in list_of_zip_tuples:
		z = Zip(zip_tuple)
		zip_list.append(z)
	return zip_list


def _validate(zipcode):
	if not isinstance(zipcode, str):
		raise TypeError('zipcode should be a string')
	int(zipcode) # This could throw an error if zip is not made of numbers
	return True

def islike(zipcode):
	"""Takes a partial zip code and returns a list of zipcode objects with matching prefixes."""
	_validate(zipcode)
	_cur.execute('SELECT * FROM ZIPS WHERE ZIP_CODE LIKE ?', ['{zipcode}%'.format(zipcode=str(zipcode))])
	return _make_zip_list(_cur.fetchall())

def isequal(zipcode):
	"""Takes a zipcode and returns the matching zipcode object.  If it does not exist, None is returned"""
	_validate(zipcode)
	_cur.execute('SELECT * FROM ZIPS WHERE ZIP_CODE == ?', [str(zipcode)])
	row = _cur.fetchone()
	if row:
		return Zip(row)
	else:
		return None

def isinradius(point, distance):
	"""Takes a tuple of (lat, lon) where lon and lat are floats, and a distance in miles. Returns a list of zipcodes near the point."""
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
	_cur.execute(stmt.format(lonmin=lonmin, lonmax=lonmax, latmin=latmin, latmax=latmax))
	results = _cur.fetchall()

	for row in results:
		if haversine(point, (row[_LAT], row[_LONG])) <= distance:
			zips_in_radius.append(Zip(row))
	return zips_in_radius



















