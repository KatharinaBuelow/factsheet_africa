# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Climate Fact Sheet Africa'
copyright = '2025, Katharina Buelow'
author = 'Katharina Buelow'
release = '2025'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
htm_title = "Factsheet Africa"

html_theme_options = {
    "repository_url":"https://github.com/KatharinaBuelow/factsheet_africa",
    "repository_branch":"main",
    "use_repository_button": True,
    "use_edit_page_button": True,
    "use_issues_button": True,
    "path_to_docs": "docs/",
    "logo_only": False,
}

html_logo = "logos/Logo_GERICS_Neu_mit_Unterzeile_EN.png"

html_static_path = ['_static']
