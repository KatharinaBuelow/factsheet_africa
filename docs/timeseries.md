# Timeseries

![image](plots/line_plot_min_max_TG_year_Burkina_Faso_ERA5.png)

Before you start, you need to create your environment by

``` console
conda env create -f plotting_fs.yml
```

To make the time series plots you use the following notebook, which uses
the funktions located in plotting_ts_tools.py . You can decide if you
like [ERA5](https://cds.climate.copernicus.eu/cdsapp#!/dataset) in the
plot or not.

``` console
$ Notebooks/TIMESERIES/plotting_ts_tools.py

$ Notebooks/TIMESERIES/timeseries_TG_WASCAL.ipynb
```

Das Notebook verwendet die Daten die in folgendem Verzeichnis liegen:

``` console
$ input_data
```
