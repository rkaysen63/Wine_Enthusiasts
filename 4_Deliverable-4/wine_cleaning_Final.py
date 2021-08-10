# Import dependencies 
import pandas as pd
#import unidecode

# Import data
wine_data_df = pd.read_csv("Data/winemag-data-130k-v2.csv")  
print(wine_data_df.shape)
wine_data_df.head()


## Select and keep only US data
# Only keep rows where country = US
US_wine_data_df = wine_data_df.loc[wine_data_df["country"] == "US"]
print(US_wine_data_df.shape)
US_wine_data_df.head()

# Drop columns that are not useful: Unnamed: 0, country, taster_name, taster_twitter_handle
US_wine_data_df = US_wine_data_df.drop(columns=["Unnamed: 0", "designation", "region_2","country","taster_name", "taster_twitter_handle"], axis=1)

# Keep California, Washington, and Oregon
WestCoast_wine_data = US_wine_data_df.loc[US_wine_data_df.province.isin(["California","Washington", "Oregon"])]
print(WestCoast_wine_data.shape)
WestCoast_wine_data.head()


## Evaluate data and clean
WestCoast_wine_data_title = WestCoast_wine_data

# Remove the region within the title
WestCoast_wine_data_title ['title'] = WestCoast_wine_data_title['title'].str.replace(r"\(.*\)","") 

# Remove the state from region
WestCoast_wine_data_title ['region_1'] = WestCoast_wine_data_title['region_1'].str.replace(r"\(.*\)","") 

# Create a region list
region_list = list(WestCoast_wine_data_title['region_1'])
print(len(region_list))
region_list

# Look at dataframe info again.
WestCoast_wine_data_title.info()

# Drop rows with NaN.  Max rows US =50259
# "price" only has 50046 rows. 
WestCoast_wine_data_title = WestCoast_wine_data_title.dropna()
print(WestCoast_wine_data_title.shape)
WestCoast_wine_data_title.head(20)


## Binning Variety, Region 
variety_counts = WestCoast_wine_data_title.variety.value_counts()
variety_counts

# Visualize the value counts of variety
variety_counts.plot.density()

replace_variety = list(variety_counts[variety_counts <= 300].index)

# Replace in dataframe
for variety in replace_variety:
    WestCoast_wine_data_title.variety = WestCoast_wine_data_title.variety.replace(variety,"Other")
    
# Check to make sure binning was successful
WestCoast_wine_data_title.variety.value_counts()

# Remove varieties where variety count <= 300
WestCoast_wine_data_title = WestCoast_wine_data_title[WestCoast_wine_data_title.variety != "Other"]
print(WestCoast_wine_data_title.shape)
WestCoast_wine_data_title.head()

# Determine value_counts for region binning
region_counts = WestCoast_wine_data_title.region_1.value_counts()
list(region_counts)

# Visualize the value counts of variety
region_counts.plot.density()

# Reduce regions list using same cut-off that was used for machine learning model.
replace_region = list(region_counts[region_counts <= 300].index)

# Replace in dataframe
for region in replace_region:
    WestCoast_wine_data_title.region_1 = WestCoast_wine_data_title.region_1.replace(region,"Other")
    
# Check to make sure binning was successful
WestCoast_wine_data_title.region_1.value_counts()

# Remove regions where region count <= 300
wine_data_df = WestCoast_wine_data_title[WestCoast_wine_data_title.region_1 != "Other"]
print(wine_data_df.shape)
wine_data_df.head()


## Categorize Wines

# Create wine categories/types column
wine_data_df["type"] = wine_data_df["variety"]

# Categorize varieties

rose = ["Rosé"]
red = ["Pinot Noir", "Cabernet Sauvignon", "Syrah", "Red Blend", "Zinfandel", "Merlot","Bordeaux-style Red Blend", 
       "Cabernet Franc", "Rhône-style Red Blend", "Petite Sirah", "Malbec", "Grenache", "Sangiovese", "Tempranillo"]
white = ["Chardonnay", "Sauvignon Blanc","Riesling","Pinot Gris","Viognier", "Sparkling Blend", "Gewürztraminer", 
         "Pinot Grigio", "White Blend"]

wine_data_df = wine_data_df.replace({"type": white},"White")
wine_data_df = wine_data_df.replace({"type": rose},"Pink")
wine_data_df = wine_data_df.replace({"type": red},"Red")
wine_data_df.head()


# Import Dependencies for Database
from config import password
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import psycopg2


db_string = f"postgresql+psycopg2://postgres:" + password + "@127.0.0.1:5434/WineEnthusiast"

engine = create_engine(db_string)

wine_data_df.to_sql(name='us_wine', con=engine, method='multi')