# Climate fact sheet for countries in West Africa
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

# 1902  conda install reportlab
# 1911  conda install numpy
# 1913  conda install scipy
# 1915  conda install six
# 1917  conda install netCDF4
# 1919  conda install pandas
# 1929  conda install conda-forge::scikit-image


  	conda env create -f env_reprtlab.yml


## Usage:

You have to execute:
    python run_script_factsheets_africa.py