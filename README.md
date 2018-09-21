# Zipcode
### A simple python package for dealing with zip codes

**IMPORTANT.** This package relies on up-to-date data from
unitedstateszipcodes.org. To ensure that this package works, please follow the
installation instructions closely, making sure that you also follow any rules
governing zipcode data distributed by unitedstateszipcodes.org as per their
site. The data is free for non-commercial use, and affordable for commercial
use, you must download it from them though as I am not allowed to distribute it.

## Installation

1. go to https://www.unitedstateszipcodes.org/zip-code-database/
2. download the CSV file, pick free or a commercial version if you need to use
   it commercially. If you need to buy the commercial one, do so, but download
   the free one as that is the one supported by this package.
3. move the downloaded file to a good location and set appropriate environment
   variables.
```bash
mkdir -p /var/lib/zipcode
mv ~/Downloads/zip_code_database.csv /var/lib/zipcode/zip_code_database.csv
echo 'ZIPS_CSV=/var/lib/zipcode/zip_code_database.csv' >> ~/.bash_profile
source ~/.bash_profile
```
4. set up the database.
  - for production applications a relational database like
   postgresql is recommended! sqlite is acceptable for lower use applications. 
 - after you decide which database to use, *find your connection string*
   [here](http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine).
```bash
# set connection string, we use sqlite as an example (but use postgres in production!)
echo 'ZIPCODE_CONNECTION_STRING=sqlite:///zipcode.db' >> ~/.bash_profile
source ~/.bash_profile
```
5. install zipcode
```bash
pip install zipcode
```
6. populate the database
  - this might take a while ~10min for postgres. be patient, it'll be fast once loaded
```bash
build_zipcode_database
```
Good to go. The next section shows you how to use the package.

## Getting started

```py
import zipcode

myzip = zipcode.isequal('44102')
myzip.state     #=> 'OH'
myzip.city      #=> 'Cleveland'
myzip.location #=> 'Cleveland, OH'

# all keys in the dictionary can also be fetched with dot notation.
dict(myzip) #=> {'zipcode': '44102', 'zipcode_type': 'STANDARD', 'city': 'Cleveland', 'state': 'OH', 'timezone': 'America/New_York', 'lat': 41.48, 'lng': -81.74, 'county': 'Cuyahoga County', 'location': 'Cleveland, OH', 'decommissioned': True, 'population': 31930, 'area_codes': ['216'], 'secondary_cities': []} 


zipcode.islike('00') #=> list of Zip objects that begin with given prefix.

cbus = (39.98, -82.98)
zipcode.isinradius(cbus, 20) #=> list of all zip code objects within 20 miles of 'cbus'

zipcode.hascity('Cleveland', 'OH') #=> list of zip codes in Cleveland, OH
zipcode.hascity('', 'OH') #=> list of zip codes in state of OH
zipcode.hascity('Flushing', 'NY', include_secondary=False) #=> don't include zips where flushing is a secondary city

zipcode.hasareacode(216) #=> list of zip codes associated with 216 
```

## Keeping the database up-to-date

Zip codes don't change very often, but the borders do change, and new zip codes
are added, and others are removed. To keep your zipcode package ever up-to-date
we suggest that you set up a job to keep the database current, or simply drop
the zipcodes table in your database and re-rerun steps 1-3 and 6 once every 3
months or so.

You're all set.  Get to it!
