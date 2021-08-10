
# Dependencies to pull API
import requests
import json
# Google developer API key
from config import gkey

# Import Dependencies for Database
import wine_cleaning_updated
from config import password
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import psycopg2
import pandas as pd
import time

db_string = f"postgresql+psycopg2://postgres:" + password + "@127.0.0.1:5434/WineEnthusiast"

engine = create_engine(db_string)
inspector = inspect(engine)
inspector.get_table_names()

connection = engine.connect
session = Session(engine)
engine.execute("SELECT * from us_wine")

col_names_list = []

for i in range(len(inspector.get_columns('us_wine'))):
    col_names_list.append(inspector.get_columns('us_wine')[i]['name'])
    
print(col_names_list)

location_wine_df = pd.DataFrame(columns = col_names_list)
location_wine_df.drop(columns = ['description', 'points', 'price', 'province',
                                 'title', 'variety', 'winery', 'type'], axis = 1)

# Inner join for wines and regions
import sys
join_db = engine.execute("SELECT DISTINCT region_1 from us_wine")
for record in join_db:
    record_series = pd.Series((record), index = location_wine_df.columns)
    
    location_wine_df = location_wine_df.append(record_series, ignore_index=True, verify_integrity = True)
    
# Display df columns
location_wine_df

# Drop unnecessary columns and duplicates
region_df = location_wine_df.drop(columns = ['index','description', 'points', 'price', 'province',
                                             'title', 'variety', 'winery','type'], axis = 1)

region_df.dropna(inplace=True)

# Create a region list
region_list = list(region_df['region_1'])
print(len(region_list))
region_list

# Build the endpoint URL
valley_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?inputtype=textquery&key='+ gkey

# Format regions to a string
regions = str(region_df)
regions.format

# Create an empty list to hold the region data.
place_id_data = []
# Print the beginning of the logging.
print("Beginning Data Retrieval     ")
print("-----------------------------")

# Create counters.
record_count = 1
set_count = 1

# Loop through all the regions in the list.
for i, region in enumerate(region_list):

 # Group regions in sets of 50 for logging purposes.
    if (i % 50 == 0 and i >= 50):
        set_count += 1
        record_count = 1
    # Create endpoint URL with each region_id.
    placeid_url = valley_url + '&input='+ region
    

    # Add a one second interval between queries to stay within API query limits
    time.sleep(1)
    
    # Log the URL, record, and set numbers and the region.
    print(f"Processing Record {record_count} of Set {set_count} | {region}")
    # Add 1 to the record count.
    record_count += 1 
    
# Run an API request for each of the regions.
    try:
        # Parse the JSON and retrieve data.
        region_url = requests.get(placeid_url).json()
        # Parse out the needed data.
        place_id = region_url['candidates'][0]['place_id']
        # Append the region information into place_id_data list.
        place_id_data.append({"region": region, 
                              "Place_id": place_id})

# If an error is experienced, skip the region.
    except:
        print("region not found. Skipping...")
        pass



# Indicate that Data Loading is complete.
print("-----------------------------")
print("Data Retrieval Complete      ")
print("-----------------------------")

# Create place_id dataframe
placeid_df = pd .DataFrame(place_id_data)
placeid_df.head(10)

# Create place_id list
place_id_list = list(placeid_df['Place_id'])
print(len(place_id_list))

# Target valley
#region = "Sonoma Valley"

# Build the endpoint URL
valley_url2 = ('https://maps.googleapis.com/maps/api/place/details/json?&key='+ gkey)

# Create an empty list to hold the coord data.
coord_id_data = []
# Print the beginning of the logging.
print("Beginning Data Retrieval     ")
print("-----------------------------")

# Create counters.
record_count = 1
set_count = 1

# Loop through all the place ids in the list.
for i, placeids in enumerate(place_id_list):

 # Group place ids in sets of 25 for logging purposes.
    if (i % 25 == 0 and i >= 25):
        set_count += 1
        record_count = 1
    # Create endpoint URL with each region_id.
    coord_url = valley_url2 + '&place_id='+ placeids
    

    # Add a one second interval between queries to stay within API query limits
    time.sleep(1)
    
    # Log the URL, record, and set numbers and the place ids.
    print(f"Processing Record {record_count} of Set {set_count} | {placeids}")
    # Add 1 to the record count.
    record_count += 1 
    
# Run an API request for the place ids and retrieve the lat long info.
    try:
        # Parse the JSON and retrieve data.
        geo_url = requests.get(coord_url).json()
        # Parse out the needed data.
        lat_id = geo_url['result']['geometry']['location']['lat']
        long_id = geo_url['result']['geometry']['location']['lng']
        # Append the region information into place_id_data list.
        coord_id_data.append({"Place_id": placeids, 
                              "Latitude": lat_id,
                             "Longitude": long_id})
        


# If an error is experienced, skip the record.
    except:
        print("record not found. Skipping...")
        pass



# Indicate that Data Loading is complete.
print("-----------------------------")
print("Data Retrieval Complete      ")
print("-----------------------------")

# Create a coordinate dataframe
coord_df = pd.DataFrame(coord_id_data)
coord_df.head(10)

# Join the place_id and coord dataframes
region_df = pd.concat([placeid_df, coord_df], axis=1, join="inner")

# Drop Place_id column
region_df = region_df.drop(['Place_id'], axis=1)
region_df

# Create connection string
db_string = f"postgresql+psycopg2://postgres:" + password + "@127.0.0.1:5434/WineEnthusiast"

# Create the database engine
engine = create_engine(db_string)

# Save the region_df DataFrame to a SQL table called wineregions
region_df.to_sql(name='wineregion', con=engine)

#region_df.to_csv("Data/region_df.csv", index=False)