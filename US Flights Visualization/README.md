## Data Visualization: Performance of 6 Largest U.S. Domestic Carriers from 2003 to 2016
by Paris Georgoudis

### Summary

This project visualized the top 20% quartile of the performance for the years 2003-2016 for the largest U.S. domestic airlines' performance from 2003-2016.  It depicts 3 charts the percentage of On-Time arrivals, the percentage of Delays due to Carrier and the average minute of Delays per Carrier. All data was collected from RITA.

### Summary of data

```
##	     year         X.month          carrier                             carrier_name   
##	 Min.   :2003   Min.   : 1.000   OO     : 21605   SkyWest Airlines Inc.       : 21605  
##	 1st Qu.:2006   1st Qu.: 4.000   EV     : 20161   ExpressJet Airlines Inc.    : 19468  
##	 Median :2009   Median : 7.000   MQ     : 17932   Delta Air Lines Inc.        : 17173  
##	 Mean   :2009   Mean   : 6.575   DL     : 17173   American Eagle Airlines Inc.: 15409  
##	 3rd Qu.:2012   3rd Qu.:10.000   AA     : 12281   American Airlines Inc.      : 12281  
##	 Max.   :2016   Max.   :12.000   UA     : 11875   Atlantic Southeast Airlines : 12204  
##	                                 (Other):107878   (Other)                     :110765  
##
##	    airport                                              airport_name     arr_flights   
##	 LAX    :  2141   Los Angeles, CA: Los Angeles International   :  2141   Min.   :    1  
##	 LAS    :  2128   Las Vegas, NV: McCarran International        :  2128   1st Qu.:   62  
##	 PHX    :  2094   Phoenix, AZ: Phoenix Sky Harbor International:  2094   Median :  136  
##	 DEN    :  2063   Denver, CO: Denver International             :  2063   Mean   :  399  
##	 SAN    :  2057   San Diego, CA: San Diego International       :  2057   3rd Qu.:  289  
##	 DTW    :  2050   Detroit, MI: Detroit Metro Wayne County      :  2050   Max.   :21648  
##	 (Other):196372   (Other)                                      :196372   NA's   :312  
##
##	   arr_del15         carrier_ct       X.weather_ct         nas_ct         security_ct    
##	 Min.   :   0.00   Min.   :   0.00   Min.   :  0.000   Min.   :  -0.01   Min.   : 0.000  
##	 1st Qu.:  12.00   1st Qu.:   4.02   1st Qu.:  0.000   1st Qu.:   2.33   1st Qu.: 0.000  
##	 Median :  27.00   Median :   9.80   Median :  0.740   Median :   6.90   Median : 0.000  
##	 Mean   :  79.83   Mean   :  22.37   Mean   :  2.916   Mean   :  27.13   Mean   : 0.194  
##	 3rd Qu.:  62.00   3rd Qu.:  21.73   3rd Qu.:  2.330   3rd Qu.:  17.85   3rd Qu.: 0.000  
##	 Max.   :6377.00   Max.   :1792.07   Max.   :717.940   Max.   :4091.27   Max.   :80.560  
##	 NA's   :352       NA's   :312       NA's   :312       NA's   :312       NA's   :312   
##
##	 late_aircraft_ct  arr_cancelled       arr_diverted       X.arr_delay     X.carrier_delay 
##	 Min.   :   0.00   Min.   :   0.000   Min.   :  0.0000   Min.   :     0   Min.   :     0  
##	 1st Qu.:   2.00   1st Qu.:   0.000   1st Qu.:  0.0000   1st Qu.:   545   1st Qu.:   189  
##	 Median :   6.94   Median :   1.000   Median :  0.0000   Median :  1368   Median :   491  
##	 Mean   :  27.20   Mean   :   6.983   Mean   :  0.9013   Mean   :  4381   Mean   :  1268  
##	 3rd Qu.:  18.97   3rd Qu.:   5.000   3rd Qu.:  1.0000   3rd Qu.:  3298   3rd Qu.:  1142  
##	 Max.   :1885.47   Max.   :1969.000   Max.   :256.0000   Max.   :433687   Max.   :134693  
##	 NA's   :312       NA's   :312        NA's   :312        NA's   :312      NA's   :312  
##
##	 weather_delay     nas_delay      security_delay     late_aircraft_delay    X          
##	 Min.   :    0   Min.   :   -19   Min.   :   0.000   Min.   :     0      Mode:logical  
##	 1st Qu.:    0   1st Qu.:    80   1st Qu.:   0.000   1st Qu.:   101      NA's:208905   
##	 Median :   32   Median :   252   Median :   0.000   Median :   400                    
##	 Mean   :  226   Mean   :  1218   Mean   :   7.236   Mean   :  1661                    
##	 3rd Qu.:  174   3rd Qu.:   692   3rd Qu.:   0.000   3rd Qu.:  1188                    
##	 Max.   :57707   Max.   :238440   Max.   :3119.000   Max.   :148181                    
##	 NA's   :312     NA's   :312      NA's   :312        NA's   :312   
```

#### Exploratory Data Analysis and Cleaning (R)

I downloaded the data from [RITA](http://www.transtats.bts.gov/OT_Delay/ot_delaycause1.asp?display=download&pn=0&month=1&year=2016). Since June 2003, the airlines report on-time data also report the causes of delays and cancellations to the Bureau of Transportation Statistics. Please see below the structure and summary of the database which was conducted using **Rstudio** and is found in detail in `data/data.Rmd` and `data/data.html`. While studying the data, I hypothesized that there might be trends in individual airline performance that can be extracted from the data. I decided that a line chart with multiple series would best show these different trends across different airlines.


##Initial Analysis


![Initial R Plot](https://github.com/parisge/Udacity/blob/master/US%20Flights%20Visualization/images/onetime_all.png)

The chart above shows my initial run to display the performance of US domestic flights in terms of their carrier on time arrival. This is such a busy figure with 28 airlines and obviously it too cluttered in delivering analysis. For the next step, I will pick only the top 20% airlines based on the yearly average arrival flights number. 

## Final Visualizations

The selected (top 20%) carriers for visualization are :

```
## [1] "American Airlines Inc."   "Delta Air Lines Inc."    
## [3] "SkyWest Airlines Inc."   "American Eagle Inc."
## [5] "Southwest Airlines Co."   "United Air Lines Inc."
```

In this project the objective is to:

To show the performance of carriers, I will aggregate data by *year* and *carrier name* and use different metrics to see how they perform over time.

The charts used will be a combination of catter plot and line chart. Using point, I can precisly display the measure and audience can easily compare. Also, I will add lines to be able to show trends of the performance and for them to see how perfomance of each carrier changed over time. 

![Final R Plot](https://github.com/parisge/Udacity/blob/master/US%20Flights%20Visualization/images/carrier_comparisons.png)

### Average Percentage of Arrivals On-Time

![% of Arrivals On-Time](https://github.com/parisge/Udacity/blob/master/US%20Flights%20Visualization/images/ontime_carrier.png)

Based on the diagram, we see that the percentage for on-time flights has converged significantly during the years 2011-2012 and 2015. For 2016 we have data only for the first month so they chart results need to be taken with a grain of salt. It is also clear from the chart is that Delta Airlines is outperfomring its competitors in terms of On-Time completed flights, even though it ranked below others before 2011.

Now let's examinte whether it is the carriers mistake the cause of the late flights. There can be multiple cause of late flighs such as Security, Weather, National Aviation System, Aircraft arriving late. The Air Carrier delay is contributing on average only 5% of the 20% on average of the plane delays. 

### Average Percentage Delay due to Carrier

![% Delays due to Carrier](https://github.com/parisge/Udacity/blob/master/US%20Flights%20Visualization/images/delays_carrier.png)

As we can see SkyWest a regional airline which partners up with United, American and Delta used to have the highest number of delayed flights due to the carrier, but has significantly dropped after 2007. In the last few years United and South West has seen an increasing number of flights getting delayed due to the carrier. 

### Average Time Delay due to Carrier

![Time Delay due to Carrier](https://github.com/parisge/Udacity/blob/master/US%20Flights%20Visualization/images/timedelay_carrier.png)

What is very interesting is that the average time of delay attributed to each carrier shows a very different picture than the Percentage of On-Time Arrivals and the Percentage of Delays due to Carrier. Delta Airlines that had on of the best records in terms of Arrivales and lowest in terms of Carrier Delays has on average the highest amount of minutes of delay. The trend on the average number of minutes of delay has been upwards, maybe because the Carriers are engaging in longer distance flights. Similarly SkyWest which saw it's Percentage Delay due to Carrier drop after 2007, it has see its Time Delay increase consistently after 2009. 


## Feedback
I showed the charts to couple of my friends and here are the main comments that I got back:


1 - "By looking at the On-Time flight rates chart, there is significant difference between carriers, however, the way you scaled the y axis doesn't really deliever the point! "

The range for percentage of on-time flight is between 65 and 100%. The diagram initially had y axis from (0 to 100%) which made a lot of empty space in the chart and also the difference of perfromance among the carriers were not really visible. I shortened the range from (0,100) to (65,100) so the difference become more obvious. 

2- "Even though the lines and points are colored differently, I think it would be really nice to highlight or emphasize individual airlines when you select them."

I added a `mouseover` event for the lines, so it would 'pop' it out and emphasize the path.  This would allow for better understanding of each individual airline's trend from 2003 to 2016.

3- "In the OnTime arrivals the dotted grid lines that come vertically to the x-axis stop at the 70% level. It would be nice to go all the way down to the x-axis."

I manually overrode the minimum Y-axis interval for the OnTime arrivals chart to be at 65%. In this way the 

4- "Using a bit lighter colors for the charts would make it more plesant to the eye. Having the right side of the chart open was nice, in addition to the points being spread apart. "

I re-adjusted the colors of the lines and points to make them less intense and nicer in the eye.

5- "In some of the charts the legend gets clustered with the data. Try to put it all the way in the top-right side of the charts"

I decided to move the legend to the top right, in this way avoiding any clustering with the data.

6- "The relationship of the graphs seems very interesting. I can clearly see who is the champion and focus comparatively on how each airline has perfomed. "

By highlighting every airline and presenting the data in the order I did I think it made it faily simple to see the relationships among the different airlines. 


Below is the final view of the data visualization:

![Final Chart](https://github.com/parisge/Udacity/blob/master/US%20Flights%20Visualization/images/final_chart.png)

### Resources

- [Data Visualization and D3.js (Udacity)](https://www.udacity.com/course/viewer#!/c-ud507-nd)
- [dimple.js Documentation](http://dimplejs.org/)
- [Scott Murray D3 Tutorials](http://alignedleft.com/tutorials/d3)
- [Mike Bostock D3 Selections](https://github.com/mbostock/d3/wiki/Selections)
- [Stator Tutoria Mouse Events](http://www.stator-afm.com/tutorial/d3-js-mouse-events/)
- Various [Stack Overflow](http://stackoverflow.com/search?q=dimple.js) posts

### Data
Data is taken from the following website on May 5, 2015:
http://www.transtats.bts.gov/OT_Delay/ot_delaycause1.asp?display=download&pn=0&month=1&year=2016

- `data/401340571_12016_2229_airline_delay_causes.csv`: original downloaded dataset
- `data/data.csv`: cleaned and truncated dataset, utilized in final dimple.js implementation
