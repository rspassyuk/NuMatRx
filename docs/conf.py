"""Build documentation without importing Qt or external nuclear datasets."""
project = "NuMatRx"
author = "NuMatRx contributors"
copyright = "2026, NuMatRx contributors"
extensions = ["myst_parser", "sphinx.ext.mathjax"]
myst_enable_extensions = ["dollarmath", "colon_fence"]
myst_heading_anchors = 3
html_theme = "sphinx_rtd_theme"
html_title = "NuMatRx documentation"
html_theme_options = {"navigation_depth": 3, "collapse_navigation": False}
html_static_path = ["_static"]
html_logo = "_static/images/numatrx_logo_light.png"
exclude_patterns = ["_build", "manual-ru.md", "**/Thumbs.db"]
source_suffix = {".md": "markdown"}
root_doc = "index"
language = "en"
