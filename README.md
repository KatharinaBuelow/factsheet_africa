# Climate factsheet for countries in West Africa
This repository contains all python scripts need to produce a climate fact sheet for a selected countra in africa

## Environment

Dies ist der automatische regional Climate-Fact-Sheet-Generator.
Er erstellt ein pdf-Dokument angelehnt an das GERICS Climate Fact Sheet Design unter Verwendung
von reportlab.
Möglichst viel ist automatisiert, so dass ein Großteil der benötigten Informationen über
Metadaten mit den Abbildungen eingelesen werden können. Angepasst werden müssen folgende Inhalte:
 - abstract
 - text_daten (Angabe der Datenquellen)
 - Seite heutiges Klima
 - Disclaimer
 - ffg. Liste der verwendeten Simulationen
Benötigt wird Regional_fact_sheets_common_modules.py. Hier sind alle Funktionen/Module ausgelagert,
benötigt auch config_Klimaausblick2020.py (muss im selben Verzeichnis liegen)

conda install reportlab
conda install numpy
conda install scipy
conda install six
conda install netCDF4
conda install pandas
conda install conda-forge::scikit-image


  	conda env create -f env_reprtlab.yml


## Usage:

You have to execute:
    python run_script_factsheets_africa.py
