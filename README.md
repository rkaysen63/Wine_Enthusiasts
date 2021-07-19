# Wine_Enthusiasts

<p align="center">
  <img src="Images/pexels-brett-sayles-1374552.jpg" width="700">
</p>

## Table of Contents
* [Overview](https://github.com/rkaysen63/Wine_Enthusiasts/blob/master/README.md#overview)
* [Resources](https://github.com/rkaysen63/Wine_Enthusiasts/blob/master/README.md#resources)
* [Results](https://github.com/rkaysen63/Wine_Enthusiasts/blob/master/README.md#results)
* [Summary](https://github.com/rkaysen63/Wine_Enthusiasts/blob/master/README.md#summary)

## Resources:    
* Data: https://www.kaggle.com/zynicide/wine-reviews?select=winemag-data-130k-v2.csv
* Tools: 
  * Python (Libraries: pandas, matplotlib, hvplot.pandas, plotly.express, sklearn.preprocessing, sklearn.decomposition, sklearn.cluster)
  * Jupyter Notebook
  * SQL
  * Tableau
* Photo Acknowledgement:
  * Sayles, Brett. https://www.pexels.com/photo/red-wine-marquee-signage-on-table-1374552/
* Lesson Plan: UTA-VIRT-DATA-PT-02-2021-U-B-TTH, Module 20: Final Project

## Overview: 
Wine Enthusiasts is an online travel app that helps users locate regions throughout the US where they can go to the source of their favorite wines.  The app allows input of various criteria such as type of wine, price, and/or rating.  

## Results:
* Data cleaning
  * Import depencies.
  * Import data. <br><br/>
    `wine_data_df = pd.read_csv("Data/winemag-data-130k-v2.csv")`
  * Only keep US data. <br><br/>
    `US_wine_data_df = wine_data_df.loc[wine_data_df["country"] == "US"]`
  * Drop columns that are not useful. <br><br/>
    `US_wine_data_df = US_wine_data_df.drop(columns=["Unnamed: 0", "country","taster_name", "taster_twitter_handle"], axis=1)`
  * Look at info. to evaluate data and decide next step. <br><br/>
    `US_wine_data_df.info()`
  * Drop "designation" a very specific location within a winery and the column has 32% null values.<br><br/>
    `US_wine_data_df = US_wine_data_df.drop(columns=["designation"], axis=1)`
  * Replace NaN in region_1 with corresponding value from same row in province. <br><br/>
    `US_wine_data_df_copy['region_1'] = US_wine_data_df.apply(lambda row: row['province'] if pd.isnull(row['region_1']) else row['region_1'], axis=1)
  * Replace NaN in region_2 with corresponding value from same row in region_1. (Code is similar to that above.)
    `province_counts = US_wine_data_df_copy.province.value_counts()`
  * Look at info again.  Only price has non-null values.  The data is now ready to drop NaN without losing too much data.
  * Drop rows with NaN.  Max rows US =54504. The "price" column only has 54226 rows.  Drop NaN will only reduce data by 1/2% <br><br/>
    `US_wine_data_df_copy = US_wine_data_df_copy.dropna()`
  * Drop additional columns that we may want back later: "description" - of flavors, i.e. tart and snappy, oaky, etc. "title" - name on the bottle; region_1, region_2.  These columns were saved in their own dataframe to add back if we decide to use them.<br><br/>
    `US_wine_data_df_ml = US_wine_data_df_copy.drop(columns=["description", "region_1", "region_2", "title"], axis=1)`
* Pre-Process data for machine learning
  * Look at unique values to determine if binning may be required.<br><br/>
    `US_wine_data_df_ml.nunique()`
  * Determine value_counts of province to look at data.  This is current "target".  It produces a list.  California is by far the greatest and most likely will create an inbalanced model.
  * Determine value_counts of "variety" column for binning. <br><br/>
    `variety_counts = US_wine_data_df_ml.variety.value_counts()`
  * Visualize the value counts of variety. <br><br/>
    `variety_counts.plot.density()`
  * Determine which values to replace.  Per the plot, we tried <500 but after looking at the results we decided that we wanted to be more inclusive since some mainstream varieties would be binned in "other".  Therefore we lowered the threshold for "other" to 300.

        replace_variety = list(variety_counts[variety_counts <= 300].index)`

        # Replace in dataframe
        for variety in replace_variety:
            US_wine_data_df_ml.variety = US_wine_data_df_ml.variety.replace(variety,"Other")

        # Check to make sure binning was successful
        US_wine_data_df_ml.variety.value_counts()
  * The same procedure for binning was applied to the "winery" column.
* Encode categorical data
  * Create variable to hold categorical columns for OneHotEncoder.<br><br/>
  
        wine_cat = ["variety", "winery"]

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

  * Split preprocessed data.

        # from sklearn.model_selection import train_test_split
        # Split preprocessed data into our features and target arrays
        #  Target
        y = US_wine_data_df_ml["province"].values
        # Features
        X = US_wine_data_df_ml.drop(["province"],axis=1).values

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


* SQL Database
* Machine Learning
* Visualization

## Summary:

[Back to the Table of Contents](https://github.com/rkaysen63/Wine_Enthusiasts/blob/master/README.md#table-of-contents)

