
# Import dependencies for ML
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

# Import Dependencies for Database
import Multi_Region_Lat_Long
from config import password
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import psycopg2
import pandas as pd

db_string = f"postgresql+psycopg2://postgres:" + password + "@127.0.0.1:5434/WineEnthusiast"

engine = create_engine(db_string)
inspector = inspect(engine)
inspector.get_table_names()
connection = engine.connect
session = Session(engine)
engine.execute("SELECT * from us_wine")

col_names_list = []

#i = 0
for i in range(len(inspector.get_columns('us_wine'))):
    col_names_list.append(inspector.get_columns('us_wine')[i]['name'])
    
for i in range(len(inspector.get_columns('wineregion'))):
    col_names_list.append(inspector.get_columns('wineregion')[i]['name'])
    
print(col_names_list)

US_wine_data_df = pd.DataFrame(columns = col_names_list)

# Inner join for wines and regions
import sys
join_db = engine.execute("SELECT * from wine inner join wineregion on wine.region_1 = wineregion.region")
for record in join_db:
    record_series = pd.Series(list(record), index = US_wine_data_df.columns)
    
    US_wine_data_df = US_wine_data_df.append(record_series, ignore_index=True)
    #print(list(record))

US_wine_data_df_copy = US_wine_data_df
US_wine_data_df_copy.head()

us_wine_data_copy = US_wine_data_df_copy
us_wine_data_copy.head()

us_wine_data_clean = us_wine_data_copy.drop(columns = ['region_1','index'])

us_wine_data_clean.drop_duplicates(inplace=True)
us_wine_data_clean.head()

# joined data set with lat long and wine
us_wine_data_clean.to_sql(name='uswine_db', con=engine, method='multi')


## Remove special characters
# Clean winery and variety column
winery_test = us_wine_data_clean['winery'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
variety_test = us_wine_data_clean['variety'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
title_test = us_wine_data_clean['title'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
description_test = us_wine_data_clean['description'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

winery_df = pd.DataFrame({'winery_clean':winery_test,'variety_clean':variety_test, 
                          'title_clean':title_test,  'description_clean':description_test})
winery_df

wine_data_clean = us_wine_data_clean.merge(winery_df, how = 'inner', left_index=True, right_index=True)
wine_data_clean.head()

# Drop duplicate columns
wine_data_clean = wine_data_clean.drop(columns=['title','description','variety','winery'])
wine_data_clean.head(5)

# Rename Columns
wine_data_clean = wine_data_clean.rename(columns={"winery_clean": "winery", "variety_clean": "variety"
                                               ,"title_clean":"title", "description_clean": "description"})

wine_data_clean.head(5)

## Pre process for machine learning
# Group wine price into bins.
price_counts = wine_data_clean.price.value_counts()
price_counts

price_counts.plot.density()

# Create price bins
price_bins = [0, 15, 30, 60, 100, 500, 5000]
wine_data_clean.groupby(pd.cut(wine_data_clean["price"], price_bins)).count()

price_bins_names = ["<$15","$15-30","$30-60","$60-100", "$100-500","too much"]

# Make a new column in dataframe for price bins.
wine_data_clean["price_bins"] = pd.cut(wine_data_clean["price"], price_bins, labels=price_bins_names)

# Check dataframe
wine_data_clean.tail()

# Re-arrange column order for wine finder display.
dashboard_wine_data_df = wine_data_clean[['province', 'region', 'Latitude', 'Longitude',
                                                 'winery', 'variety', 'type', 'title', 'points',
                                                 'price', 'price_bins','description']]
print(dashboard_wine_data_df.shape)
dashboard_wine_data_df.head(1)

#Export data to csv
dashboard_wine_data_df.to_csv("Data/US_Wine_PriceBins.csv", index=False)


## Code to Create JSON file
# Import dependencies
import pandas as pd
import json

# For "wine picker" drop columns
json_wine_data_df = dashboard_wine_data_df.drop(["Latitude", "Longitude", "price_bins"], axis=1)
print(json_wine_data_df.shape)
json_wine_data_df.head(1)

# Export Pandas DataFrame to JSON File
# https://datatofish.com/export-pandas-dataframe-json/
json_wine_data_df.to_json(r'static\json\data.json', orient='records')


## Create Dataframe for Machine Learning

# Create a DataFrame to hold columns ("description", "price", "province", "region_2", "title", "winery")
# that won't be used in machine learning in case we want them later.
US_wine_data_title_df = wine_data_clean.drop(columns=["points", "region", "variety","price_bins"], axis=1)
print(US_wine_data_title_df.shape)
US_wine_data_title_df.head()

# Export data with price bins
# Save cleaned columns ("description", "price", "province", "region_2", "title", "winery","latitude", "longitude")
US_wine_data_title_df.to_sql(name='winedata', con=engine)

# Create DataFrame for machine learning model. Drop: "description" - of flavors, i.e. tart and snappy, 
# oaky, etc., price, province, region_2, "title" - name on the bottle, winery.
# Dropped lat and long

US_wine_data_df_ml = US_wine_data_df.drop(columns=["description", "price", "region", "province", "region_2", "title", "winery", "Latitude", "Longitude", "Place_id"], axis=1)
print(US_wine_data_df_ml.shape)
US_wine_data_df_ml.head()

# Export data for ML: (columns for machine learning: "points","region_1",""variety","price_bins")
US_wine_data_df_ml.to_sql(name='winedata_ml', con=engine)


### Checkpoint

# Look at unique values to see if categorical data requires binning
US_wine_data_df_ml.nunique()

# Determine value_counts for binning
variety_counts = US_wine_data_df_ml.variety.value_counts()
variety_counts

# Visualize the value counts of variety
variety_counts.plot.density()

# Determine which values to replace.  Per the plot, we tried <500 but after looking
# results we decided that we wanted to be more inclusive since some mainstream wines
# would be binned in "other".  Therefore we lowered the threshold for other to 300.
replace_variety = list(variety_counts[variety_counts <= 300].index)

# Replace in dataframe
for variety in replace_variety:
    US_wine_data_df_ml.variety = US_wine_data_df_ml.variety.replace(variety,"Other")
    
# Check to make sure binning was successful
US_wine_data_df_ml.variety.value_counts()


# Determine value_counts for binning
region_1_counts = US_wine_data_df_ml.region_1.value_counts()
region_1_counts

# Visualize the value counts of region_1
region_1_counts.plot.density()

# From the plot the curve breaks around 500.
replace_region_1 = list(region_1_counts[region_1_counts <= 300].index)

# Replace in dataframe
for region_1 in replace_region_1:
    US_wine_data_df_ml.region_1 = US_wine_data_df_ml.region_1.replace(region_1,"Other")
    
# Check to make sure binning was successful
US_wine_data_df_ml.region_1.value_counts()

### Encode categorical data

# Create variable to hold categorical columns for OneHotEncoder
wine_cat = ["variety", "region_1"]

# from sklearn.preprocessing import OneHotEncoder
# Create a OneHotEncoder instance
enc = OneHotEncoder(sparse=False)

# Fit and transform the OneHotEncoder using the categorical variable list
encode_df = pd.DataFrame(enc.fit_transform(US_wine_data_df_ml[wine_cat]))

# Add the encoded variable names to the dataframe
encode_df.columns = enc.get_feature_names(wine_cat)
encode_df.shape
encode_df.head()

# Merge one-hot encoded features and drop the originals
US_wine_data_df_ml = US_wine_data_df_ml.merge(encode_df,left_index=True, right_index=True)
US_wine_data_df_ml = US_wine_data_df_ml.drop(wine_cat,axis=1)
print(US_wine_data_df_ml.shape)
US_wine_data_df_ml.head()

# Save preprocessed dataframe to csv for future reference.
US_wine_data_df_ml.to_csv("Data/US_wine_data_enc.csv", index=False)


### Split preprocessed data 

# from sklearn.model_selection import train_test_split
# Split preprocessed data into our features and target arrays
#  Target
y = US_wine_data_df_ml["price_bins"].values
# Features
X = US_wine_data_df_ml.drop(["price_bins"],axis=1).values

# Split the preprocessed data into a training and testing dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# from sklearn.preprocessing import StandardScaler
# Create a StandardScaler instances
scaler = StandardScaler()

# Fit the StandardScaler
X_scaler = scaler.fit(X_train)

# Scale the data
X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)

print(X_train_scaled [0:5])


## Machine Learning

### Try RandomForestClassifier

# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
# Create a random forest classifier. 
rf_model = RandomForestClassifier(n_estimators=500, random_state=1) 

# Fitting the model
rf_model = rf_model.fit(X_train_scaled, y_train)

# Making predictions using the testing data.
y_pred = rf_model.predict(X_test_scaled)

# Display the confustion matrix
# from sklearn.metrics import confusion_matrix
confusion_matrix(y_test, y_pred)

# Calculate the accuracy score
# from sklearn.metrics import accuracy_score, classification_report
acc_score = accuracy_score(y_test, y_pred)

# Displaying results
print(f"Accuracy Score : {acc_score}")
print("Classification Report")
print(classification_report(y_test, y_pred))