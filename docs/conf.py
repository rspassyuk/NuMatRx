"""Sphinx configuration for the NuMatRx documentation (docs).

The build imports the numerical backend (``core``, ``nuclear_data``) for the
API reference, but never the Qt GUI or external nuclear-data files.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "NuMatRx"
author = "N. Kenzhebayev, M. Khassanov, R. Spassyuk, D. Anarbek, Y. Aimuratov, M. Abishev"
copyright = "2026, Fesenkov Astrophysical Institute"

extensions = [
    "myst_parser",
    "sphinx.ext.mathjax",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_design",
    "sphinx_copybutton",
]

myst_enable_extensions = ["dollarmath", "amsmath", "colon_fence", "deflist", "attrs_inline", "attrs_block", "fieldlist"]
myst_heading_anchors = 3

source_suffix = {".md": "markdown"}
root_doc = "index"
language = "en"
exclude_patterns = ["_build", "**/Thumbs.db"]

# --- API reference -----------------------------------------------------------
autodoc_mock_imports = ["PyQt5", "matplotlib", "endf"]
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_default_options = {"members": True, "undoc-members": False, "show-inheritance": False}
napoleon_numpy_docstring = True
napoleon_google_docstring = False
# Source docstrings use free-form text; do not fail the build on their layout.
suppress_warnings = ["docutils"]

# --- HTML --------------------------------------------------------------------
html_theme = "furo"
html_title = "NuMatRx"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_theme_options = {
    "light_logo": "images/numatrx_logo_light.png",
    "dark_logo": "images/numatrx_logo_dark.png",
    "sidebar_hide_name": True,
    "source_repository": "https://github.com/rspassyuk/NuMatRx/",
    "source_branch": "main",
    "source_directory": "docs/",
    "light_css_variables": {
        "color-brand-primary": "#1f5f8b",
        "color-brand-content": "#1f5f8b",
    },
    "dark_css_variables": {
        "color-brand-primary": "#6cb4e4",
        "color-brand-content": "#6cb4e4",
    },
}
copybutton_prompt_text = r"^(\$ |>>> |PS> )"
copybutton_prompt_is_regexp = True

# --- Cross-references to Python and NumPy -------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "scipy": ("https://docs.scipy.org/doc/scipy", None),
}
