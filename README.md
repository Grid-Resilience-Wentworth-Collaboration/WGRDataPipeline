# WGRDataPipeline
Data pipeline snippets for Wentworth grid resiliency projects. 

# Pipeline 1, Price Forcasting

In this project, we are attempting to forecast the price of electricity that grid operators/power companies will
settle in the Day Ahead Marketplace for Locational Marginal Prices (LMP). You can read more about it, for example, [here](https://www.iso-ne.com/participate/support/faq/lmp#:~:text=of%20the%20LMP%3F-,What%20is%20locational%20marginal%20pricing%3F,limits%20of%20the%20transmission%20system.).

We use data available from gridstatus.io, the California ISO database, and data from tomorrow.io to gather data for 
forcasting.

The Day Ahead Market sets the price of electricity in $/MWh 24 hours ahead of when the actual transfer of electricity occurs. We want to 
predict what the price will be one more day head. For example, on 2024-Jun-07 at 8:40 AM Pacific time, the Day Ahead Market price of electricty at the node 
`EMBRCDR_2_N104` near San Francisco, CA was $24.23 per MWh. We want to forcast this price on 2024-Jun-06, 8:40 AM and get as close as we can.

![Day Ahead Market Example](./screenshots/CAISO%20DayAhead%20Map%20Screenshot%202024-06-07%20at%2011.43.56 AM.png)

Let's call this LMP_DAM(t, node) where t == 2024-Jun-07 at 8:40 AM Pacific time. For the first pass, we will use the Day Ahead Market data available to 2024-Jun-06, 8:40 AM PT. We have hourly data available on LMP for the currrent time for the given node. We will use the day till 2024-Jun-06, and create a forcast 

LMP_DAM_FORECAST(t, node), where t ==  2024-Jun-07 at 8:40 AM Pacific time. But, we are only allowed to use data to LMP_DAM(t-24 hours, ...). We are allowed to use data from other locations and any other data to this t-24 hours time from other sources. For example, we are experimenting with using weather data from tomorrow.io.

## Pipeline 1, data formats


