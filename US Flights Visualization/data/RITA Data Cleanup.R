library('ggplot2')
library('dplyr')
library('gridExtra')
library('XLConnect')
library('sp')
library('RColorBrewer')
library('reshape')
library('ggthemes')
library('reshape2')
library('scales')
library('stats')

setwd("/Users/GEP/Documents/OneDrive/Academic/Udacity/Data_Vis_Code_Files/US Flights Visualization/data")
      
data <- read.csv('401340571_12016_2229_airline_delay_causes.csv', header=TRUE)
months <- c('Jan','Feb','Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep','Oct',
                  'Nov', 'Dec')
str(data)
summary(data)
head(data)
      
data$date <- as.Date(paste(df$year, df$X.month, 1, sep='-'), format="%Y-%m-%d")
summary(data$date)
      
nrow(table(data$carrier))
      
# make a new summary table
data_mod <- data %>%
  group_by(date, year, carrier_name) %>%
  summarize(arrivals = sum(arr_flights),
            delayed = sum(arr_del15),
            cancelled = sum(arr_cancelled),
            diverted = sum(arr_diverted),
            car_delays = sum(carrier_ct),
            av_delay =sum(X.arr_delay)/sum(arr_del15),
            av_car_delay=sum(X.carrier_delay)/sum(arr_del15)) %>%
  transform(on_time = 1 - delayed/arrivals)
data_mod$percent_car_delays=data_mod$car_delays/data_mod$arrivals  
  
      
# delete NA values
data_mod <- data_mod[complete.cases(data_mod),]
ggplot(data = data_mod,
        aes(x = date, y = on_time)) +
        geom_line(aes(color = carrier_name))

# aggregate by carrier name
data_agg <- data_mod %>%
  group_by(carrier_name) %>%
  summarize(monthly_avg = mean(arrivals),
            arrivals = sum(arrivals),
            on_time = mean(on_time),
            av_delay = mean(av_delay),
            av_car_delay = mean(av_car_delay))

# pull over 80th percentile, by monthly average arrivals
largest_carriers <- subset(data_agg, monthly_avg >= quantile(monthly_avg, 0.81))$carrier_name
ontime_carriers <-subset(data_agg, on_time >= quantile(on_time, 0.81))$carrier_name
largest_carriers
ontime_carriers

data_final1 <- subset(data_mod, is.element(carrier_name, largest_carriers)) %>%
  group_by(year, carrier_name) %>%
  summarize(arrivals = sum(arrivals),
            delayed = sum(delayed),
            cancelled = sum(cancelled),
            diverted = sum(diverted),
            car_delays = sum(car_delays),
            av_delay =mean(av_delay),
            av_car_delay=mean(av_car_delay)) %>%
  transform(on_time = 1 - delayed/arrivals)
data_final1$percent_car_delays=data_final1$car_delays/data_final1$arrivals  
data_final1 <- data_final1[complete.cases(data_final1),]

data_final2 <- subset(data_mod, is.element(carrier_name, ontime_carriers)) %>%
  group_by(year, carrier_name) %>%
  summarize(arrivals = sum(arrivals),
            delayed = sum(delayed),
            cancelled = sum(cancelled),
            diverted = sum(diverted),
            car_delays = sum(car_delays),
            av_delay =mean(av_delay),
            av_car_delay=mean(av_car_delay)) %>%
  transform(on_time = 1 - delayed/arrivals)
data_final2$percent_car_delays=data_final2$car_delays/data_final2$arrivals  
data_final2 <- data_final2[complete.cases(data_final2),]

summary(data$year)

p1 <- ggplot(data = data_final1,
             aes(x = year, y = on_time)) +
  geom_line(aes(color = carrier_name)) +
  scale_x_continuous(limits=c(2003, 2016), breaks=c(2003:2016))

p2 <- ggplot(data = data_final1,
             aes(x = year, y = percent_car_delays)) +
  geom_line(aes(color = carrier_name)) +
  scale_x_continuous(limits=c(2003, 2016), breaks=c(2003:2016))

p3 <- ggplot(data = data_final1,
             aes(x = year, y = av_car_delay)) +
  geom_line(aes(color = carrier_name)) +
  scale_x_continuous(limits=c(2003, 2016), breaks=c(2003:2016))

grid.arrange(p1, p2,p3, ncol=1)


write.csv(data_final1, file="data.csv", row.names=FALSE)
