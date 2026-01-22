.. _`climate indicators`:

Climate indicators
==================

The climate parameters used are calculated with the GERICS `index_calculator`_ berechnet. *Index Calculator* uses xclim_.

+-------+----------------------------+---------------------------+---------+
| Index | Name                       | Variable                  | Output  |
+=======+============================+===========================+=========+
|  TG   | Mean temperature           | Temperature               | Year    |
+-------+----------------------------+---------------------------+---------+
|  FD   | Number of frost days       | Minimumtemperature < 0°C  | Year    |
+-------+----------------------------+---------------------------+---------+
|  SU30 | Number of heat days        | Maximumtemperature > 30°C | Year    |
+-------+----------------------------+---------------------------+---------+
|  SU35 | Numer of heat days         | Maximumtemperatur > 35°C  | Year    |
+-------+----------------------------+---------------------------+---------+
|  RRm  | mean daily precipitation   | Precipitation             | Year    |
+-------+----------------------------+---------------------------+---------+
|       |                            |                           | Season  |
+-------+----------------------------+---------------------------+---------+
|  DD   | Number of dry days         | Precipitation < 1mm/day   | Year    |
+-------+----------------------------+---------------------------+---------+
|       |                            |                           | Season  | 
+-------+----------------------------+---------------------------+---------+
|  DSx  | Maximum length of dry days | Precipitation             | Year    |
+-------+----------------------------+---------------------------+---------+
|       | Länge >= 5 Tage            |                           |         |
+-------+----------------------------+---------------------------+---------+
|  DSf  | Number of dry periods      | Precipitation             | Year    |
+-------+----------------------------+---------------------------+---------+
|       | Length >= 5 Tage           |                           |         |
+-------+----------------------------+---------------------------+---------+
|  HSx  | Max. length of heat wave   | Maximumtemperature >30°C  | Year    |
+-------+----------------------------+---------------------------+---------+
|       | Length >= 3 Tage           |                           |         |
+-------+----------------------------+---------------------------+---------+
|  HSf  | Number of heat waves       | Maximumtemperature >30°C  | Year    |
+-------+----------------------------+---------------------------+---------+
|       | Length >= 3 Tage           |                           |         |
+-------+----------------------------+---------------------------+---------+

**Tabelle xx** lists the climate parameter calculated on the basis of CORDEX AFRICA and ERA5 data.




.. _`index_calculator`: https://github.com/climate-service-center/index_calculator

.. _xclim: https://github.com/Ouranosinc/xclim
