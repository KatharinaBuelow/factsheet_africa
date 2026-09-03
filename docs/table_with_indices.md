# Indizes for ERA5 and Climate Simulations for different time slices

Each climate indicator shown in Table 3 has been supplemented with an
expert assessment describing the reliability of the results. This is
indicated by different shades of gray in the table: “the darker the
gray, the clearer the climate change.” If the majority of climate model
results for an indicator show a statistically significant increase or
decrease, the change is referred to as “robust” (dark gray). If most
model results do not show clear changes but indicate a definite
direction of change, there is a “tendency toward increase or decrease”
(gray). If the climate model results are roughly evenly split between
showing an increase and a decrease, there is no clear change (light
gray/uncertain). Below the median of all climate simulation results
(shown here in bold and large), there is an indication of the range of
possible developments in the form of a minimum and maximum change.

![image](../../PLOTS/Table_Burkina_Faso_median_grey_300.png)

**Table 3** lists the selected climate indicators and their projected
average changes for the time slice 2031-2060 and 2069-2098 compared to
the period 1991–2020. The first column shows the average observed value
over the years 1991–2020
([ERA5](https://cds.climate.copernicus.eu/cdsapp#!/dataset)). The
climate changes were calculated using the whole range of models, with
results falling between the specified minimum and maximum (Min–Max).
Above this range is the median value, with half of the models lying
below and half above it. This table can be generated using the following
notebook:

``` console
$ Notebooks/INDICES-TABLE/create_index_table_africa.ipynb
```

The Notebook is using the data:

``` console
$ input_data
```
