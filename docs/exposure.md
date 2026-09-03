# Population Exposure to Extremes in Africa

The exposure of the population (chapter `population`) to extreme climate
indicators (chapter `climate indicators`) for Africa based on
[CORDEX-CORE_AFR22](https://cordex.org/experiment-guidelines/cordex-cmip5/cordex-core/cordex-core-simulations/)
data. More information about CORDEX-CORE is described in the following
papers[^1],[^2],[^3]). For calculating the exposure the workflow
described in the paper by [Weber](https://doi.org/10.1029/2019EF001473)
is followed.

## Future Population

The detailed information about data source of the population and the
scenarios can be found in the `population` chapter.

With the following Notebook you can remap the population files and
calculate the country sum .

> Notebooks/remap_population_to_afr22.ipynb

For this notebook [xesmf](https://xesmf.readthedocs.io/en/stable/) is
neccessary or you can use the *afrheat* environment. See Chapter
`environments` for more details.

## Exposure

The change of population and the climate change signal for specific
indicators are combined. Detailed information about the expouser
calcuation is also described in the papers[^4],[^5],[^6] .

The exposure of the population to extreme event and their possible futre
changes is calculated following the formular:

``` math
\Delta E = P_r \times \Delta C + C_r \times \Delta P + \Delta C \times \Delta P
```

### Exposure calculation and plotting

The environment to create the plots in the factsheet:

``` bash
conda env create -f plotting_fs.yml
```

The following Notebook produces the horizontal exposure maps for
ssp1/rcp2 and ssp3/rcp85 of population to extrem days. The plots show
the timeslice.

``` bash
Notebooks/HORIZONTAL/horiplot-exposure-diff-robust.ipynb
```

functions are used from:

``` bash
Notebooks/plotting_tools_exposure.py

Notebooks/plotting_tools_africa.py

Notebooks/format_data_tools.py

Notebooks/colors_indices.py
```

## References

[^1]: Giorgi, F., and Coauthors, 2022: The CORDEX-CORE EXP-I Initiative:
    Description and Highlight Results from the Initial Analysis. Bull.
    Amer. Meteor. Soc., 103, E293–E310,
    <https://doi.org/10.1175/BAMS-D-21-0119.1>.

[^2]: *Remedio, A.R.; Teichmann, C.; Buntemeyer, L.; Sieck, K.; Weber,
    T.; Rechid, D.; Hoffmann, P.; Nam, C.; Kotova, L.; Jacob, D.
    Evaluation of New CORDEX Simulations Using an Updated
    Köppen–Trewartha Climate Classification. Atmosphere 2019, 10, 726.
    https://doi.org/10.3390/atmos10110726*

[^3]: Teichmann, C., Jacob, D., Remedio, A.R. et al. Assessing mean
    climate change signals in the global CORDEX-CORE ensemble. Clim Dyn
    57, 1269–1292 (2021). <https://doi.org/10.1007/s00382-020-05494-x>\*

[^4]: Weber, T., Bowyer, P., Rechid, D., Pfeifer, S., Raffaele, F.,
    Remedio, A. R., et al. (2020). Analysis of compound climate extremes
    and exposed population in Africa under two different emission
    scenarios. Earth's Future, 8, e2019EF001473.
    <https://doi.org/10.1029/2019EF001473>

[^5]: Liu, Z., Anderson, B., Yan, K. et al. Global and regional changes
    in exposure to extreme heat and the relative contributions of
    climate and population change. Sci Rep 7, 43909 (2017).
    <https://doi.org/10.1038/srep43909>

[^6]: Jones, B., O’Neill, B., McDaniel, L. et al. Future population
    exposure to US heat extremes. Nature Clim Change 5, 652–655 (2015).
    <https://doi.org/10.1038/nclimate2631>
