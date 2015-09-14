A simple python package for dealing with zip codes
==================================================

Simple package for dealing with zip codes in python.
    >>> import zipcode
    >>> 
    >>> myzip = zipcode.isequal('44102')
    >>> myzip.state     #=> 'OH'
    >>> myzip.city      #=> 'Cleveland'
    >>> 
    >>> myzip.to_dict() #=>  {'zip_type': u'STANDARD', 'city': u'CLEVELAND', 'population': u'27699', 'zip': u'44102', 'yaxis': u'-0.74',     'location_text': u'Cleveland, OH', 'country': u'NA', 'notes': u'', 'lon': -81.67, 'tax_returns_filed': u'17409', 'state': u'OH', 'z    axis': u'0.66', 'location': u'NA-US-OH-CLEVELAND', 'xaxis': u'0.1', 'lat': 41.47, 'wages': u'408225500', 'decommisioned': u'FALSE',     'location_type': u'PRIMARY', 'world_region': u'NA'}
    >>>  
    >>> #all keys in the dictionary can be fetched with dot notation.
    >>> 
    >>> zipcode.islike('00') #=> list of Zip objects that begin with given prefix.
    >>> 
    >>> cbus = (39.98, -82.98)
    >>> zipcode.isinradius(cbus, 20) #=> list of all zip code objects within 20 miles of 'cbus'


