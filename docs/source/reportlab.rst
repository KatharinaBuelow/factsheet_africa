Introduction to reportlab
=========================

This is the automatic regional Climate Fact Sheet generator.
It creates a PDF document based on the GERICS Climate Fact Sheet design using ReportLab.
As much as possible is automated so that most of the required information can be read automatically. 

It contains all Introduction and todays climate in

.. code-block:: console

   title_page_africa.py
   
followed by individual pages for temperature, precipitation, compound events and finally all background information. All pages need to be stored reportlab as well as the template and the run_script, e.g.:

.. code-block:: console
		
   $ reportlab/page_temperature.py/


Usage
-----

You have to execute:

.. code-block:: console
		
   $ python run_script_factsheets_africa.py
   



Environment
^^^^^^^^^^^

conda install reportlab
conda install numpy
conda install scipy
conda install six
conda install netCDF4
conda install pandas
conda install conda-forge::scikit-image

.. code-block:: bash
		
   conda env create -f factsheet.yml

Also see chapter :ref:`environments`. 


