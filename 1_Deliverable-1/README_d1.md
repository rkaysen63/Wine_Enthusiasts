# Wine Enthusiasts Winery

<p align="center">
  
![pexels-brett-sayles-1374552](https://github.com/rkaysen63/Wine_Enthusiasts/blob/main/Images/pexels-brett-sayles-1374552.jpg)

</p>

## Table of Contents
* [Overview](https://github.com/rkaysen63/Wine_Enthusiasts/blob/master/README.md#overview)
* [Setup](https://github.com/rkaysen63/Wine_Enthusiasts/blob/master/README.md#setup)
* [Process](https://github.com/rkaysen63/Wine_Enthusiasts/blob/master/README.md#process)
* [Results](https://github.com/rkaysen63/Wine_Enthusiasts/blob/master/README.md#results)
* [Summary](https://github.com/rkaysen63/Wine_Enthusiasts/blob/master/README.md#summary)

## Overview
### Description
This project is reviewing wine data for trends. Due to the large volume of data available, we will be using various data analysis techniques to analyze the data and will provide visualizations to make the data easy to understand.
### Background
Some executives from Wine Enthusiast magazine have decided to start a winery. They know the world of wine and are confident they can create a great wine. But it's a wide world so the challenge is deciding where to start. They understand the existing wines and wineries but aren't sure how best to fit into the wine market. They contacted us for help making determinations about what varietals to start with, what they can charge, and even what location to consider for their winery.

## Setup
### Description of source data
To begin assessing the project, we used initial data from Wine Enthusiast magazine. This data was originally scraped from Wine Enthusiast using a web scraper. For our purposes, we started with a verified and corrected data set of Wine Enthusiast data available on kaggle 
This initial data contains basic details of wines:
* Wine identification detail: designation, varietal, winery
* Evaluation details: price, points, reviewer information
* Location: province, country 
### Data focus
#### Points
Ratings of the wine are given in points on a 100-point scale. Scores are determined on both on production quality and how well the wine fits the varietal and region. Wine Enthusiast magazine reviews wines with scores above 80 points. Due to the brand recognition of the Wine Enthusiasts, the winery will only produce very high quality wine, 90 points or more. 

#### Price
Similarly, the Wine Enthusiast winery will be a high-end destination winery. The price point will be high by design, as the execs intend to build a winery and need to pay for it! One of the main question they want to answer from the data is what price range they should set for their initial offerings. They know from their industry background what existing wineries can charge for a new wine, but they need help understanding what price category they should include in their budget. 

#### Location
The Wine Enthusiasts know the US wine market and most of the partners already live in the US. For these reasons, their initial focus is the United States. However, the partners plan to move where they start the winery. They hope that the data analysis will help them decide where to begin their location search.

### Communication protocols (Internal: remove before presentation)
Like the Wine Enthusiasts, our project team are not all located in the same place. This requires us to have good communication in order to complete the project on schedule. In order to ensure that we give the best possible work on the project, we established some communication protocols.
#### Regular meetings
In our initial meeting, we compared calendars and discovered that our team had many weekend commitments during the course of this project. While we were confident that we could accomplish a lot with everyone working individually, we decided that a regular standing meeting was the best way to ensure that we are able to adjust our process as we learn more from the data provided. Monday evenings was the best day for gathering the entire team so we have a standing meeting during the duration of the project.
#### Ad hoc meetings
Our team is collaborative and we work with some overlap. This is planned to ensure that the project is completed even if things come up for individual team members and also to ensure that all members of our team get to develops and build their skills for future projects. For this overlap to work smoothly, team members set up one-on-one meetings as collaborations occur. This ensures that good feedback in each stage and allows for team meetings to focus on the big picture. 
#### Github repository
Our team established a central location for sharing code, resources, data, etc. Team members have their own folders to house any individual pieces created, but all team members can access others' information as needed. As we complete stages, we collaborate on internal or external deliverables and move progress to the main shared folder.
#### Online chat
We also report progress and ask questions on a team chat. This is mainly done as a handoff before a member's availability is limited, but we also use chat to share resources and announce additions to our group repository that might be useful to other team members.
 
### Machine Learning Model (draft, deliverable 2)

#### Preliminary feature selection and engineering 
  * Remove non-US data for initial review
  * Remove reviewer columns (taster name and twitter handle)
  * Drop "designation" (alternate version of name, often missing)
  * Adjust region data (Pull Province to region field(s) where empty. Necessary for machine learning)
  * Drop rows with empty values (Small reduction necessary for clean data)

#### Preliminary data processing
* Review data
  * Review unique values for potential target data
  * Take value counts to confirm expected issues in data
    * Confirmed that using location as a machine learning feature might create an inbalanced model.
        * US wines outnumber other countries in the Wine Enthusiast ratings
        * California wines outnumber other US states as well
  * Review, create, and edit features used in model
    * Visualize the value counts of variety
    * Review data to determine which values to combine as Other. (Necessary for machine learning model)
        * Per the plot, initial value caused some mainstream varieties to be binned in "other", so we lowered the threshold for "other" to 300 wines in that variety.
* Prepare the data for processing 
  * Create columns to hold machine learning data results
  * Encode data using OneHotEncoder, fit and transform the data (adjust values to variables for use by machine learning model)
  * Adjust the working dataset to contain only fields used by machine learning model
* Prepare for machine learning 
    * Split preprocessed data into our features (examined) and target (results) arrays
    * Split the preprocessed data into a training and testing dataset
    * Scale the dataset to set values on a consistent scale across columns for even evaluation
    * Fit the data and run initial evaluations

#### Machine Learning model choice
* Models considered
    * Easy Ensemble Classifier (EEC) 
    * Random Forest Classifier (RFC)
* Models chosen: RFC
    * Advantages
        * robust against overfitting as the weak learners are trained on different pieces of the data.
        * can be used to rank the importance of input variables in a natural way.
        * can handle thousands of input variables without variable deletion.
        * robust to outliers and nonlinear data.
        * run efficiently on large datasets.
    * In Testing, RFC outperformed the EEC.
        * We ran both models ten times, and the results for both were consistent and reproducible with accuracy scores staying around 0.6027861723299182 for the RFC and 0.39787685396188066 for the EEC.
        * The RFC ran on average five seconds faster than the EEC. 

<p align="center">
  
![ML_Test](https://github.com/rkaysen63/Wine_Enthusiasts/blob/main/1_Deliverable-1/ML_Test.PNG)

![RFC_Mockup](https://github.com/rkaysen63/Wine_Enthusiasts/blob/main/1_Deliverable-1/RFC_Mockup.PNG)

</p>

### Description of Database (draft/deliverable 2)
* Database chosen: SQL via PGadmin
  * Advantages
    * Convenience: All team members have access to PG Admin
    * INTERNAL: Future projects: Using Wine Enthusiast or other branded connection might limit our future use of the project for training or template purposes

* Tables
  * Wine Enthusiast Data
  * Location table
  * Internal: Add results table and any other features added 
  * ERD
  
<p align="center">
  
![ERD](https://github.com/rkaysen63/Wine_Enthusiasts/blob/main/1_Deliverable-1/ERD.png)


![WineMag_DB](https://github.com/rkaysen63/Wine_Enthusiasts/blob/main/1_Deliverable-1/WineMag_DB.png)


![WineRegions](https://github.com/rkaysen63/Wine_Enthusiasts/blob/main/1_Deliverable-1/WineRegions.png)

</p>
 
## Process (to come/2)
### Analysis Phase
description of analysis phase
### Internal: Tools Used (draft, deliverable 2)
Description of tools used: Technologies, languages, tools, algos used
* Data: https://www.kaggle.com/zynicide/wine-reviews?select=winemag-data-130k-v2.csv
* Tools: 
  * Python (Libraries: pandas, matplotlib, hvplot.pandas, plotly.express, sklearn.preprocessing, sklearn.decomposition, sklearn.cluster)
  * Jupyter Notebook
  * SQL
  * TBD for dashboard: Tableau/webpage 

### Planning the Presenation
Google slide draft of presentation
#### Required slides

#### INTERNAL: To do list for next phase of Slides
1. Find images
2. Set color scheme
3. Determine how to make slides appear as public when shared (Outline roughly follows readme)


## Results (to come/4)
### Results
Result
### Recommendations
Rec for future analysis
### Internal: Lessons Learned
Anything to do differently




