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
        return "{}, {}".format(self.city, self.state)

    @property
    def secondary_cities(self):
        result = self._secondary_cities.replace(', ', ',').split(",")
        if len(result) == 1 and result[0]=='':
            return []
        else:
            return result

    @secondary_cities.setter
    def secondary_cities(self, value):
        self._secondary_cities = value

    @property
    def area_codes(self):
        result =  self._area_codes.replace(', ',',').split(",")
        if len(result) == 1 and result[0]=='':
            return []
        else:
            return result

    @area_codes.setter
    def area_codes(self, value):
        self._area_codes = value

    def __repr__(self):
        return '<Zip {}>'.format(self.zipcode)

    def __iter__(self):
        """Implements dict()"""
        yield ('zipcode', self.zipcode)
        yield ('zipcode_type', self.zipcode_type)
        yield ('city', self.city)
        yield ('state',self.state)
        yield ('timezone', self.timezone)
        yield ('lat', self.lat)
        yield ('lng', self.lng)
        yield ('county', self.county)
        yield ('location', self.location)
        yield ('decommissioned', self.decommissioned)
        yield ('population', self.estimated_population)
        yield ('area_codes', self.area_codes)
        yield ('secondary_cities', self.secondary_cities)



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
    session = Session()
    zips = session.query(Zip).filter(Zip.zipcode.like("%{}%".format(str(zipcode)))).all()
    session.close()
    return zips 

def isequal(zipcode):
    """Takes a zipcode and returns the matching zipcode object.  If it does not exist, None is returned"""
    _validate(zipcode)
    session = Session()
    result = session.query(Zip).filter(Zip.zipcode == str(zipcode)).one()
    session.close()
    if result:
        return result 
    else:
        return None

def hasareacode(areacode):
    areacode = str(areacode)
    session = Session()
    zips = session.query(Zip).filter(Zip._area_codes.like("%{}%".format(str(areacode)))).all()
    session.close()
    return zips

def hascounty(county):
    session = Session()
    zips = session.query(Zip).filter(Zip.county.like("%{}%".format(str(county)))).all()
    session.close()
    return zips 

def hascity(city, state="", include_secondary=True):
    """Given a city name and 2 letter state code, return associated zip codes"""
    session = Session()
    if include_secondary:
        zips = session.query(Zip)\
            .filter( (Zip.city.like("%{}%".format(str(city)))) |
                    (Zip._secondary_cities.like("%{}%".format(str(city))))
                   )\
            .filter(Zip.state.like("%{}%".format(str(state))))\
            .all()
    else:
        zips = session.query(Zip)\
            .filter( Zip.city.like("%{}%".format(str(city))))\
            .filter(Zip.state.like("%{}%".format(str(state))))\
            .all()

    session.close()
    return zips 

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

    session = Session()
    zips = session.query(Zip)\
        .filter(Zip.lng > lngmin)\
        .filter(Zip.lng < lngmax)\
        .filter(Zip.lat > latmin)\
        .filter(Zip.lat < latmax)\
        .all()
    session.close()

    for z in zips:
        if haversine(point, (z.lat, z.lng)) <= distance:
            zips_in_radius.append(z)
    return zips_in_radius


