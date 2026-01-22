Calculation of Statistical Significance and Robustness of Climate Change Signals
================================================================================

An ensemble of climate simulations is employed to account for uncertainties in model projections and to enhance the robustness of the results.

Uncertainties_ in climate modeling arise from the inherent complexity of the climate system and its interactions, the necessary simplifications of climate processes within models (including numerical parameterization due to computational constraints), natural climate variability, and assumptions regarding future trajectories of greenhouse gas concentrations, aerosols, and land-use patterns.
The statistical significance of projected climate changes is assessed for each individual simulation using a formal hypothesis-testing approach. This procedure evaluates whether an observed change exceeds the range of random (natural) variability. In this context, a climate change is considered statistically significant if, according to the `Mann-Whitney-U-Test`_, the likelihood of it being attributable to random fluctuations is less than 5%.


Expert Assessment
-----------------
The results of the selected model ensemble are accompanied by information on statistical significance and robustness. Calculations were performed using xclim_.

**Robust Increase:** At least two-thirds of the simulations indicate an increase, and at least 50% of the simulations show a statistically significant increase.

**Robust Decrease:** At least two-thirds of the simulations indicate a decrease, and at least 50% of the simulations show a statistically significant decrease.

**Tendency Toward Increase:** At least two-thirds of the simulations indicate an increase, but fewer than 50% show a statistically significant increase.

**Tendency Toward Decrease:** At least two-thirds of the simulations indicate a decrease, but fewer than 50% show a statistically significant decrease.

**Uncertain:** No two-thirds majority regarding the direction of change, but at least 50% of the simulations show statistically significant changes.

**No Change:** No two-thirds majority regarding the direction of change, and fewer than 50% of the simulations show statistically significant changes.



.. _xclim: https://github.com/Ouranosinc/xclim

.. _`Mann-Whitney-U-Test`: https://de.wikipedia.org/wiki/Wilcoxon-Mann-Whitney-Test

.. _`Uncertainties`: https://link.springer.com/chapter/10.1007/978-3-662-66696-8_5#Sec3
