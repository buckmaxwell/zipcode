__author__ = 'Max Buck'
__email__ = 'maxbuckdeveloper@gmail.com'
__license__ = 'MIT'
__package__ = 'zipcode'
__version__ = '4.0.0'

from haversine import haversine
from sqlalchemy import (create_engine, Column, Integer, String, Float, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import math
import os


try:
    conn_str = os.environ['ZIPCODE_CONNECTION_STRING']
except KeyError:
    raise Exception('ZIPCODE_CONNECTION_STRING not set, \n'
            'http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine')


Base = declarative_base()
engine = create_engine(conn_str)
Session = sessionmaker(bind=engine)

class Zip(Base):
    __tablename__ = 'zipcodes'
    
    zipcode = Column(String, primary_key=True)
    zipcode_type = Column(String)
    city = Column(String)
    state = Column(String)
    timezone = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    _secondary_cities = Column(String)
    county = Column(String)
    decommissioned = Column(Boolean)
    estimated_population = Column(Integer)
    _area_codes = Column(String) 

    @property
    def location(self):
        "{}, {}".format(self.city, self.state)

    @property
    def secondary_cities(self):
        return self._secondary_cities.split(", ")

    @secondary_cities.setter
    def secondary_cities(self, value):
        self._secondary_cities = value

    @property
    def area_codes(self):
        return self._area_codes.split(", ")

    @area_codes.setter
    def area_codes(self, value):
        self._area_codes = value

    def __repr__(self):
        return '<ZipCode {}>'.format(self.zipcode)

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


