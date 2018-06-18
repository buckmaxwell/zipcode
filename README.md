# Zipcode
### A simple python package for dealing with zip codes


**IMPORTANT.** This package uses up-to-date data from unitedstateszipcodes.org.
If you wish to use this package for non-commercial purposes, please do! If you
are using this as part of a commercial purpose, that is fine too, but before you
do, you must buy a license to use this data from unitedstateszipcodes.org,
[here](https://www.unitedstateszipcodes.org/zip-code-database/) - the license
will be 40-200 dollars depending on the size of your business.


## Getting started

Simple package for dealing with zip codes in python.  
Full documentation at https://pythonhosted.org/zipcode

    >>> import zipcode
    >>> 
    >>> myzip = zipcode.isequal('44102')
    >>> myzip.state     #=> 'OH'
    >>> myzip.city      #=> 'Cleveland'
    >>> 
    >>> dict(myzip) #=> {'zip_type': u'STANDARD', 'city': u'Cleveland', 'decommissioned': 0, 'zip': u'44102', 'state': u'OH', 'secondary_cities': [u''], 'location': 'Cleveland, OH', 'area_codes': [u'216'], 'lat': 41.48, 'timezone': u'America/New_York', 'lng': -81.74, 'population': 31930} 
    >>>  
    >>> #all keys in the dictionary can be fetched with dot notation.
    >>> 
    >>> zipcode.islike('00') #=> list of Zip objects that begin with given prefix.
    >>> 
    >>> cbus = (39.98, -82.98)
    >>> zipcode.isinradius(cbus, 20) #=> list of all zip code objects within 20 miles of 'cbus'
    >>>
    >>>
    >>> zipcode.hascity('Cleveland', 'OH') #=> list of zip codes in Cleveland, OH
    >>> zipcode.hascity('', 'OH') #=> list of zip codes in OH
    >>>
    >>>
    >>> zipcode.hasareacode(216) #=> list of zip codes associated with 216 

## Keeping the database up-to-date

Zip codes don't change very often, but the borders do change, and new zip codes
are added, and others are removed. To keep your zipcode package ever up-to-date
we suggest that you set up a job to keep the sqlite3 database current.

You'll pull the latest version of the database from our server once a month, and
copy it to the install location of your current sqlite3 database. 

```bash
$ pip show zipcode
Name: zipcode
Version: 3.0.0
Summary: A simple python package for dealing with  zip codes in python.
Home-page: https://github.com/buckmaxwell/zipcode
Author: Max Buck
Author-email: maxbuckdeveloper@gmail.com
License: MIT
Location: /<YOUR/<PATH>
Requires: haversine
```

Note the location line. This is the top level of your version of the zipcode
package. If the whole thing were set to a variable, the database would live at
$LOCATION/zipcode.db - and look something like
/<YOURPATH>/site-packages/zipcode/zipcode.db. For the next part imagine the
whole path to the database is set to $DB_PATH. 

Now, take the following and modify the user agent to a value of your choice. The
user agent must begin with robot.  We ask that you limit your download requests
to monthly - the database will not change more often than that. You can copy the
script and put it in your crontab or a script that is run by your crontab.

```bash
wget -d --header="User-Agent: robot/<SOME UNIQUE NAME>"  https://maxwellbuck.com/downloads/zipcode.db.gz
gunzip zipcode.db.gz
cp zipcode.db $DB_PATH
```

Your all set.  Get to it!
