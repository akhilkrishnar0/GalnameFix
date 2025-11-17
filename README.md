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


## Example
```
from galnamefix import process_galaxy_catalog, choose_primary
import pandas as pd

df = process_galaxy_catalog("prg_36-for_public.csv")
df['PRIMARY_NAME'] = df.apply(choose_primary, axis=1)
df.head()
```

## 📄 LICENSE
```text
MIT License
```



