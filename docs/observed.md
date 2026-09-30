# Temperatur and Precipitation anomaly

Example Burkina Faso 
 
<img src="/assets/ERA5_Annual_anomaly_deviation_to_1991_2020_Burkina_Faso_nc.png"
     alt="ERA5 annual anomaly deviation to 1991–2020 for Burkina Faso"
     width="360">


**Figure 1** The figure shows annual temperature and precipitation
anomalies for Burkina Faso from 1941 to 2023, based on ERA5 reanalysis
data. The anomalies are calculated relative to the 1991–2020 reference
period, which is indicated by the vertical dashed lines. In the upper
panel, temperature anomalies (in °C) reveal a clear long-term warming
trend. Most years before the 1980s were cooler than the reference
period, with anomalies often below –1 °C, especially during the 1950s
and 1960s. Starting in the late 1980s, anomalies approach zero, and from
the 2000s onward, nearly all years are warmer than the 1991–2020
average. The most recent decade shows persistent positive anomalies,
exceeding +1 °C in several years, highlighting significant warming
compared to the reference period. The lower panel displays
precipitation anomalies (in %). Early decades, particularly the 1940s
and 1950s, were generally wetter than the reference period, with
anomalies reaching +40 % or more. From the 1970s onward, negative
anomalies become more frequent, indicating drier conditions relative to
1991–2020. The Sahel drought period in the 1980s is evident, with
anomalies below –20 %. Recent years show mixed variability, but overall,
precipitation tends to show high annual variability. This visualization
underscores that the 1991–2020 reference period itself is already warmer
than earlier decades, meaning current anomalies represent additional
warming beyond an already elevated baseline.

Figure 1 can be created with the following Notebook:

``` console
$ Notebooks/ERA5/Plot_ERA5_annual_anomaly-new_color.ipynb
```

The Notebook uses the aggregated data:

``` console
$ input_data/eobs
```

Data source: ERA5 global reanalysis ([Hersbach et al.,
2020](https://doi.org/10.24381/cds.bd0915c6)).
