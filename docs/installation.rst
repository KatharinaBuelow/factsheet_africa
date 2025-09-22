Installation
============

To set up the Factsheet Africa environment, you have several options:

Using Conda Environment
-----------------------

The recommended way is to use the provided conda environment file:

.. code-block:: bash

   conda env create -f env_reprtlab.yml
   conda activate reprtlab

Manual Installation
-------------------

Alternatively, install the required packages manually:

.. code-block:: bash

   conda install reportlab
   conda install numpy
   conda install scipy
   conda install six
   conda install netCDF4
   conda install pandas
   conda install conda-forge::scikit-image

Requirements
------------

- Python 3.x
- reportlab
- numpy
- scipy
- six
- netCDF4
- pandas
- scikit-image
   
