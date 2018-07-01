# Dash Data Visualisation Project

This project is created using Plotly's dash framework. 

This is a single-page web application.

## Data Used

The data points are a set of values recorded each hour everyday. This historical data was used to predict the historical values acording to the trend as well as the data for future dates. At present, data till 30-04-2018 was used to predict data till 29-07-2018.

1. Monthly Data
  * Data recorded for each day of the month
  * Organised as DD-MM-YYYY
  
 2. Daily Data
  * Data recorded for each hour of the day
  * Recorded as DD-MM-YYYY HH:MM:SS
  
 3. Criterion - A
  * Data is broken into 4 categories according to some criterion
  * Recorded as DD-MM-YYYY HH:MM:SS
  
 4. Criterion -B
  * Data is broken into 4 categories according to some criterion
  * Recorded as DD-MM-YYYY HH:MM:SS
  
  ## Graphs
  
Every kind of data has a graph associated with it. 

  > Monthly Data has a graph showing Actual Values and Predicted Values, input being a date range
  
  > Daily Data has a graph showing same values, alongwith a table showing the same data, input being a single date
  
  > Criterion - A data has a graph showing same values in 4 adjacent graphs, updated simultaneously with an input being a date range
  
  > Criterion - B same as Criterion - A

## Libraries

Libraries used are saved in the [**requirements.txt**](../requirements.txt) file.

To install all the libraries directly, navigate to the directory and run the command

```pip3 install -r requirements.txt```





---
Other projects: [Parangat](https://github.com/thesciencestudent) 
