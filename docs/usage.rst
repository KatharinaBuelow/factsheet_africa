Usage
=====

To generate a climate factsheet for an African country, execute the main script:

.. code-block:: bash

   python run_script_factsheets_africa.py

Example Usage
-------------

Here's how the main script works:

.. code-block:: python

   from reportlab_template_africa import *

   # Configuration
   final_pdf_name = 'Test_Burkina_Faso_reportlab.pdf'
   region = 'Burkina Faso'
   anzahl_simulationen = 18
   version = '1'
   
   # Logo paths
   gerics_logo = 'logos/Logo_GERICS_Neu_mit_Unterzeile_EN.png'
   bmbf_logo = 'logos/BMFTR_en_DTP_CMYK_gef_durch.jpg'
   wascal_logo = 'logos/WASCAL_Logo.png'
   
   # Create and generate factsheet
   doc = FactSheet(final_pdf_name, version, region, gerics_logo, 
                   wascal_logo, bmbf_logo, basic_color, sprache, 
                   cs_orange, cs_schwarz, title_image_burkinafaso, 
                   box_era5, table_cc, anzahl_simulationen)
   
   doc.createDocument()
   doc.savePDF()

Configuration
-------------

The following elements need to be customized:

- abstract
- text_daten (data source information)
- current climate page
- disclaimer
- list of simulations used

The system requires ``Regional_fact_sheets_common_modules.py`` and 
``config_Klimaausblick2020.py`` to be in the same directory.