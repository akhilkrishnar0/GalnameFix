# GalnameFix


**GalnameFix** is a Python tool that selects the *best galaxy name* from multiple catalogs based on:
- coordinate consistency (within `max_sep` arcseconds)
- prefix priority (NGC > IC > PGC > UGC > ESO ...)
- automatic catalog detection


## Features
- Works with any combination of catalogs (SIMBAD, NED, LVD, HyperLeda, etc.)
- Automatically detects which catalogs exist in each row
- Ensures the selected name corresponds to consistent coordinates
- Fully customizable prefix order


## Installation
pip install .


## 📄 LICENSE
```text
MIT License
```



