# WGRDataPipeline
Data pipeline snippets for Wentworth grid resiliency projects. 

1. [Pipeline 1](#pipeline-1-price-forcasting)
    - [Pipeline 1 Data Formats](#pipeline-1-data-formats)
    - [Pipline 1, modules](#pipline-1-modules)

# Pipeline 1, Price Forcasting

In this project, we are attempting to forecast the price of electricity that grid operators/power companies will
settle in the Day Ahead Marketplace for Locational Marginal Prices (LMP). You can read more about it, for example, [here](https://www.iso-ne.com/participate/support/faq/lmp#:~:text=of%20the%20LMP%3F-,What%20is%20locational%20marginal%20pricing%3F,limits%20of%20the%20transmission%20system.).

We use data available from gridstatus.io, the California ISO database, and data from tomorrow.io to gather data for 
forcasting.

The Day Ahead Market sets the price of electricity in $/MWh 24 hours ahead of when the actual transfer of electricity occurs. We want to 
predict what the price will be one more day head. For example, on 2024-Jun-07 at 8:40 AM Pacific time, the Day Ahead Market price of electricty at the node 
`EMBRCDR_2_N104` near San Francisco, CA was $24.23 per MWh. We want to forcast this price on 2024-Jun-06, 8:40 AM and get as close as we can.

![Day Ahead Market Example](./screenshots/CAISO%20DayAhead%20Map%20Screenshot%202024-06-07%20at%2011.43.56 AM.png)

Let's call this LMP_DAM(t, node) where t == 2024-Jun-07 at 8:40 AM Pacific time. For the first pass, we will use the Day Ahead Market data available to 2024-Jun-06, 8:40 AM PT. We have hourly data available on LMP for the currrent time for the given node. We will use the day till 2024-Jun-06, and create a forcast.

LMP_DAM_FORECAST(t, node), where t ==  2024-Jun-07 at 8:40 AM Pacific time. But, we are only allowed to use data to LMP_DAM(t-24 hours, ...). We are allowed to use data from other locations and any other data to this t-24 hours time from other sources. For example, we are experimenting with using weather data from tomorrow.io.

## Pipeline 1, data formats

### LMP Data

The LMP Data are avaiable at a given folder in our file system, where data for each date are stored in CSV file named by date. For example, `2024-05-16.csv` contains data from 2024-May-16. The have the columns shown the following figure. The -7 indicates offset from UTC Time for this data.

![LMP Data Example](./screenshots/LMP%20Data%20Example%20Screenshot%202024-06-07%20at%2012.15.08 PM.png)

### Co-ordinates data

The latitute-longitude co-ordiantes for a given nodes are stored in another folder in a JSON file with a given name. An example is shown below.

![Node Location Example](./screenshots/Node%20Location%20Example%20Screenshot%202024-06-07%20at%2012.22.51 PM.png)

### Weather data

The weather data from API at tomorrow.io are stored in another folder where JSON files are stored with a node name and a timestamp, for example, `BLKDIA_7_N001-2024-05-29 08:14:40.078147.json`. The weather forcast data are avaiable per minute, hour and day. The data in these files look like the following. Note that the timestamps could be in a different timezone than the LMP data.

```JSON
{
  "timelines": {
    "minutely": [
      {
        "time": "2024-05-29T12:14:00Z",
        "values": {
          "cloudBase": null,
          "cloudCeiling": null,
          "cloudCover": 0,
          "dewPoint": 5.88,
          "freezingRainIntensity": 0,
          "humidity": 51,
          "precipitationProbability": 0,
          "pressureSurfaceLevel": 1016,
          "rainIntensity": 0,
          "sleetIntensity": 0,
          "snowIntensity": 0,
          "temperature": 15.88,
          "temperatureApparent": 15.88,
          "uvHealthConcern": 0,
          "uvIndex": 0,
          "visibility": 16,
          "weatherCode": 1000,
          "windDirection": 253,
          "windGust": 8.13,
          "windSpeed": 5.69
        }
      },
```

```JSON
"daily": [
      {
        "time": "2024-05-28T13:00:00Z",
        "values": {
          "cloudBaseAvg": 0.27,
          "cloudBaseMax": 1.88,
          "cloudBaseMin": 0,
          "cloudCeilingAvg": 0.08,
          "cloudCeilingMax": 1.87,
          "cloudCeilingMin": 0,
          "cloudCoverAvg": 6.17,
          "cloudCoverMax": 59,
          "cloudCoverMin": 0,
          "dewPointAvg": 7.96,
          "dewPointMax": 10.63,
          "dewPointMin": 5.31,
          "evapotranspirationAvg": 0.28,
          "evapotranspirationMax": 0.687,
          "evapotranspirationMin": 0.055,
          "evapotranspirationSum": 6.441,
          "freezingRainIntensityAvg": 0,
          "freezingRainIntensityMax": 0,
          "freezingRainIntensityMin": 0,
          "humidityAvg": 47.04,
          "humidityMax": 73,
          "humidityMin": 37,
          "iceAccumulationAvg": 0,
          "iceAccumulationLweAvg": 0,
          "iceAccumulationLweMax": 0,
          "iceAccumulationLweMin": 0,
          "iceAccumulationLweSum": 0,
          "iceAccumulationMax": 0,
          "iceAccumulationMin": 0,
          "iceAccumulationSum": 0,
          "moonriseTime": "2024-05-28T07:39:03Z",
          "moonsetTime": "2024-05-28T17:33:50Z",
          "precipitationProbabilityAvg": 0,
          "precipitationProbabilityMax": 0,
          "precipitationProbabilityMin": 0,
          "pressureSurfaceLevelAvg": 1014.64,
          "pressureSurfaceLevelMax": 1016.63,
          "pressureSurfaceLevelMin": 1013.53,
          "rainAccumulationAvg": 0,
          "rainAccumulationLweAvg": 0,
          "rainAccumulationLweMax": 0,
          "rainAccumulationLweMin": 0,
          "rainAccumulationMax": 0,
          "rainAccumulationMin": 0,
          "rainAccumulationSum": 0,
          "rainIntensityAvg": 0,
          "rainIntensityMax": 0,
          "rainIntensityMin": 0,
          "sleetAccumulationAvg": 0,
          "sleetAccumulationLweAvg": 0,
          "sleetAccumulationLweMax": 0,
          "sleetAccumulationLweMin": 0,
          "sleetAccumulationLweSum": 0,
          "sleetAccumulationMax": 0,
          "sleetAccumulationMin": 0,
          "sleetIntensityAvg": 0,
          "sleetIntensityMax": 0,
          "sleetIntensityMin": 0,
          "snowAccumulationAvg": 0,
          "snowAccumulationLweAvg": 0,
          "snowAccumulationLweMax": 0,
          "snowAccumulationLweMin": 0,
          "snowAccumulationLweSum": 0,
          "snowAccumulationMax": 0,
          "snowAccumulationMin": 0,
          "snowAccumulationSum": 0,
          "snowDepthAvg": 0,
          "snowDepthMax": 0,
          "snowDepthMin": 0,
          "snowDepthSum": 0,
          "snowIntensityAvg": 0,
          "snowIntensityMax": 0,
          "snowIntensityMin": 0,
          "sunriseTime": "2024-05-28T12:58:00Z",
          "sunsetTime": "2024-05-29T03:11:00Z",
          "temperatureApparentAvg": 19.9,
          "temperatureApparentMax": 25.5,
          "temperatureApparentMin": 14.63,
          "temperatureAvg": 19.9,
          "temperatureMax": 25.5,
          "temperatureMin": 14.63,
          "uvHealthConcernAvg": 1,
          "uvHealthConcernMax": 3,
          "uvHealthConcernMin": 0,
          "uvIndexAvg": 2,
          "uvIndexMax": 8,
          "uvIndexMin": 0,
          "visibilityAvg": 16,
          "visibilityMax": 16,
          "visibilityMin": 16,
          "weatherCodeMax": 1000,
          "weatherCodeMin": 1000,
          "windDirectionAvg": 252.13,
          "windGustAvg": 10.42,
          "windGustMax": 13.5,
          "windGustMin": 7.69,
          "windSpeedAvg": 6.43,
          "windSpeedMax": 7.69,
          "windSpeedMin": 4.88
        }
      },
```

```JSON
    "hourly": [
      {
        "time": "2024-05-29T12:00:00Z",
        "values": {
          "cloudBase": null,
          "cloudCeiling": null,
          "cloudCover": 0,
          "dewPoint": 5.88,
          "evapotranspiration": 0.061,
          "freezingRainIntensity": 0,
          "humidity": 51,
          "iceAccumulation": 0,
          "iceAccumulationLwe": 0,
          "precipitationProbability": 0,
          "pressureSurfaceLevel": 1016.63,
          "rainAccumulation": 0,
          "rainAccumulationLwe": 0,
          "rainIntensity": 0,
          "sleetAccumulation": 0,
          "sleetAccumulationLwe": 0,
          "sleetIntensity": 0,
          "snowAccumulation": 0,
          "snowAccumulationLwe": 0,
          "snowDepth": 0,
          "snowIntensity": 0,
          "temperature": 16,
          "temperatureApparent": 16,
          "uvHealthConcern": 0,
          "uvIndex": 0,
          "visibility": 16,
          "weatherCode": 1000,
          "windDirection": 252.88,
          "windGust": 8.19,
          "windSpeed": 5.81
        }
      },
```

## Pipline 1, modules

### Data Gatherer

Gathers data for training and analysis. To run, make sure you are in the right python environment, and have 
an approriate .evn. Run the Data Gatherer code.
```bash
cd src
python RunDataGatherer.py
```

### Data availability

The data availability module takes as input a given `Node ID`, a given timestamp in UTC and outputs whether data are avaiable for a given set of tolerance values. For example, if the node is `EMBRCDR_2_N104`, and the time is `2024-05-29 13:00`, the module will scan the provided folders to look for whether LMP data is avaiable for the date `2024-05-29` and any number of days before this timestamp as provided in the tolerate inputs. It will also check whether weather forcast data are avaiable for this date by looking at whether a file exists in the weather forcast folder with the right name. A further extension, in the future, could look for data availability for nearby nodes.

Parameters:

1. Node ID
2. Datetime
1. Datetime tolerance (in minutes)
    - This parameter determines whether the very first data point avaiable is within the given tolerance of minutes
2. History (in hours)
    - This parameter determines if data is avaiable for at least given number of days in the past from the given date/time

### Series Creator

The series creater module takes as input a given `Node ID`, a given timestamp in UTC and outputs a series of data that can be used as input to 
the forcaster. The series output is a JSON file with the following fields:

1. LMP Historical
    - time
    - LMP
2. Weather Forcast

The output of the series creator is a JSON file that resides in the folder from the `SERIES_FOLDER` environment variable. In version 1, the series folder has files named in the format `NodeID_DateTime.json`. For example, `EMBRCDR_2_N104_2024-05-29-1300+0700.json`. The series data is readied to be fed to the LLM for forcast. As we experiment with forcast accuracy, we will need to experiment with this output format, but we will always have prior versions in the code available for comparison.


