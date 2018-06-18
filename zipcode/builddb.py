# -*- coding: utf-8 -*-
#from __future__ import unicode_literals, print_function

import csv
import sqlite3
import os


db_filename = 'zip.db'
directory = os.path.dirname(os.path.abspath(__file__))
zipcodedb_location = os.path.join(directory, db_filename)
conn = sqlite3.connect(zipcodedb_location, check_same_thread=False)

cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS "ZIPS" (
  "ZIP_CODE" TEXT,
  "ZIP_CODE_TYPE" TEXT,
  "CITY" TEXT,
  "STATE",
  "TIMEZONE" TEXT,
  "LAT" REAL,
  "LONG" REAL,
  "SECONDARY_CITIES" TEXT,
  "COUNTY" TEXT,
  "DECOMMISSIONED" BOOLEAN,
  "ESTIMATED_POPULATION" INT,
  "AREA_CODES" TEXT
  );'''
)

with open('zips_20180617.csv') as f:
    reader = csv.reader(f)
    """zip,type,decommissioned,primary_city,acceptable_cities,
    unacceptable_cities,state,county,timezone,area_codes,
    world_region,country,latitude,longitude,
    irs_estimated_population_2015"""
    for row in reader:
        print(row)

        
        db_row = []
        db_row.append(row[0]) # zip
        db_row.append(row[1]) # zip type 
        db_row.append(row[3]) # city
        db_row.append(row[6]) # state
        db_row.append(row[8]) # timezone
        db_row.append(row[12]) # lat
        db_row.append(row[13]) # long
        db_row.append(row[4]) # secondary cities 
        db_row.append(row[7]) # county
        db_row.append(row[2]) # decommissioned 
        db_row.append(row[14]) # long
        db_row.append(row[9]) # timezone

        cur.execute('''INSERT INTO ZIPS (ZIP_CODE, ZIP_CODE_TYPE, CITY, STATE,
        TIMEZONE, LAT, LONG, SECONDARY_CITIES, COUNTY, DECOMMISSIONED,
        ESTIMATED_POPULATION, AREA_CODES) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?)''',
        db_row)

conn.commit()
