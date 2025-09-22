#! /usr/bin/python

# Configuration file for the Sphinx documentation builder.

project = 'factsheet_africa'
author = 'Katharina Buelow'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',    # For docstrings
    'sphinx.ext.napoleon',   # For Google/NumPy style docstrings
    'sphinx.ext.viewcode',   # Adds "view source" links
]

templates_path = ['_templates']
exclude_patterns = []

# HTML output
html_theme = 'alabaster'  # or 'sphinx_rtd_theme' if installed
html_static_path = ['_static']
