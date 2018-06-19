__author__ = 'Max Buck'
__email__ = 'maxbuckdeveloper@gmail.com'
__license__ = 'MIT'
__package__ = 'zipcode'
__version__ = '3.0.1'


import sqlite3 as db
import os
from haversine import haversine
import math

_db_filename = 'zipcode.db'
_directory = os.path.dirname(os.path.abspath(__file__))
_zipcodedb_location = os.path.join(_directory, _db_filename)
_conn = db.connect(_zipcodedb_location, check_same_thread=False)


_cur = _conn.cursor()

# positions
_ZIP_CODE = 0 # => "44102"
_ZIP_CODE_TYPE = 1 # => "STANDARD"
_CITY= 2 # => "Cleveland"
_STATE = 3 # => "OH"
_TIMEZONE = 4 # => "America/New_York"
_LAT = 5 # => "40.81"
_LONG = 6 # => "-73.04"
_SECONDARY_CITIES = 7 # => ""
_COUNTY = 8 #  => "Cuyahoga County"
_DECOMMISSIONED = 9 # => False
_ESTIMATED_POPULATION = 10 # => 31930
_AREA_CODES = 11 # => "216" or "419,567"

class Zip(object):
    """The zip code object."""
    def __init__(self, zip_tuple):

        # The 5 digit zipcode TODO: pad front of zips with 0s
        self.zip = zip_tuple[_ZIP_CODE]

        # The type of zipcode accoroding to USPS: UNIQUE, PO BOX, STANDARD
        self.zip_type = zip_tuple[_ZIP_CODE_TYPE]

        # primary city associated w zip
        self.city = zip_tuple[_CITY]

        self.state = zip_tuple[_STATE]

        # America/New_York -> possible future support for other tz
        # formats => https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        self.timezone = zip_tuple[_TIMEZONE]

        # The lat/lng associated with the zipcode according to the
        # National Weather Service.  This can be empty when there is no
        # NWS Data"
        self.lat = zip_tuple[_LAT]
        self.lng = zip_tuple[_LONG]

        # The city with its state or territory => 'Cleveland, OH' or 'Anasco, PR'"""
        self.location = "{}, {}".format(zip_tuple[_CITY], zip_tuple[_STATE])

        # a list of non-primary cities that are also acceptable
        self.secondary_cities = zip_tuple[_SECONDARY_CITIES].split(", ")

        self.county = zip_tuple[_COUNTY]

        # A boolean value that reveals if a zipcode is still in use
        self.decommissioned = zip_tuple[_DECOMMISSIONED]

        # Estimated population
        self.population = zip_tuple[_ESTIMATED_POPULATION]

        # Area codes
        self.area_codes = zip_tuple[_AREA_CODES].split(",")

    def __repr__(self):
        return '<Zip: {zip}>'.format(zip=self.zip)

        def __iter__(self):
            """Implements dict()"""
            yield ('zip', self.zip)
            yield ('zip_type', self.zip_type)
            yield ('city', self.city)
            yield ('state',self.state)
            yield ('timezone', self.timezone)
            yield ('lat', self.lat)
            yield ('lng', self.lng)
            yield ('county', self.county)
            yield ('location', self.location)
            yield ('decommissioned', self.decommissioned)
            yield ('population', self.population)
            yield ('area_codes', self.area_codes)
            yield ('secondary_cities', self.secondary_cities)


def _make_zip_list(list_of_zip_tuples):
    zip_list = list()
    for zip_tuple in list_of_zip_tuples:
        z = Zip(zip_tuple)
        zip_list.append(z)
    return zip_list


def _validate(zipcode):
    if not isinstance(zipcode, str):
        raise TypeError('zipcode should be a string')
        try:
            int(zipcode)
        except:
            raise TypeError('zicode should be convertable to int')

        if int(zipcode) > 99999:
            raise TypeError('zipcode should be 5 digits or less')
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

def hasareacode(areacode):
    areacode = str(areacode)
    _cur.execute('SELECT * FROM ZIPS WHERE AREA_CODES LIKE ?', ['%{}%'.format(areacode)])
    return _make_zip_list(_cur.fetchall())

def hascounty(county):
    _cur.execute('SELECT * FROM ZIPS WHERE COUNTY LIKE ?', ['%{}%'.format(areacode)])
    return _make_zip_list(_cur.fetchall())

def hascity(city, state=""):
    """Given a city name and 2 letter state code, return associated zip codes"""
    _cur.execute('SELECT * FROM ZIPS WHERE CITY LIKE ? AND STATE LIKE ?',
            ['%{}%'.format(city), '%{}%'.format(state)])
    return _make_zip_list(_cur.fetchall())

def isinradius(point, distance):
    """Takes a tuple of (lat, lng) where lng and lat are floats, and a distance in miles. Returns a list of zipcodes near the point."""
    zips_in_radius = list()
    
    if not isinstance(point, tuple):
        raise TypeError('point should be a tuple of floats')
    for f in point:
        if not isinstance(f, float):
            raise TypeError('lat and lng must be of type float')

    dist_btwn_lat_deg = 69.172
    dist_btwn_lng_deg = math.cos(point[0]) * 69.172
    lat_degr_rad = float(distance)/dist_btwn_lat_deg
    lng_degr_rad = float(distance)/dist_btwn_lng_deg

    latmin = point[0] - lat_degr_rad
    latmax = point[0] + lat_degr_rad
    lngmin = point[1] - lng_degr_rad
    lngmax = point[1] + lng_degr_rad

    if latmin > latmax:
        latmin, latmax = latmax, latmin
    if lngmin > lngmax:
        lngmin, lngmax = lngmax, lngmin

    stmt = ('SELECT * FROM ZIPS WHERE LONG > {lngmin} AND LONG < {lngmax}\
     AND LAT > {latmin} AND LAT < {latmax}')
    _cur.execute(stmt.format(lngmin=lngmin, lngmax=lngmax, latmin=latmin, latmax=latmax))
    results = _cur.fetchall()

    for row in results:
        if haversine(point, (row[_LAT], row[_LONG])) <= distance:
            zips_in_radius.append(Zip(row))
    return zips_in_radius


