
from astropy.coordinates import SkyCoord
import astropy.units as u

def choose_primary(row, max_sep=10, PREFIX_PRIORITY=None, get=None, get_prefix=None):
    if PREFIX_PRIORITY is None:
        PREFIX_PRIORITY = ["NGC", "IC", "PGC", "UGC", "ESO", "MCG", "MRK", "VCC", "LEDA"]

    if get is None:
        get = lambda row, key: row[key] if isinstance(row, dict) else getattr(row, key, None)

    if get_prefix is None:
        get_prefix = lambda name: name.split()[0].upper() if name else None

    # Determine all catalogs
    if isinstance(row, dict):
        keys = row.keys()
    else:
        keys = row.__dict__.keys()

    catalogs = []
    for key in keys:
        if key.startswith("OBJNAME_"):
            catalogs.append(key.replace("OBJNAME_", ""))

    catalogs = sorted(set(catalogs))

    if not catalogs:
        return None

    # Build coordinate list
    coords = {}
    for cat in catalogs:
        ra = get(row, f"RA_{cat}")
        dec = get(row, f"DEC_{cat}")
        if ra is not None and dec is not None:
            coords[cat] = SkyCoord(ra * u.deg, dec * u.deg)

    # If fewer than 2 have coordinates → fallback
    if len(coords) < 2:
        for cat in catalogs:
            n = get(row, f"OBJNAME_{cat}")
            if n:
                return n
        return None

    # Determine which catalogs agree
    consistent = set()
    cat_list = list(coords.keys())
    for i in range(len(cat_list)):
        for j in range(i + 1, len(cat_list)):
            a, b = cat_list[i], cat_list[j]
            if coords[a].separation(coords[b]).arcsec < max_sep:
                consistent.add(a)
                consistent.add(b)

    # If consistent catalogs exist
    if consistent:
        cons_names = [get(row, f"OBJNAME_{cat}") for cat in consistent]

        # Prefix priority
        for pref in PREFIX_PRIORITY:
            for name in cons_names:
                if name and get_prefix(name) == pref:
                    return name

        # Fallback inside consistent
        for cat in catalogs:
            if cat in consistent:
                n = get(row, f"OBJNAME_{cat}")
                if n:
                    return n

    # No consistent catalogs → global fallback
    for cat in catalogs:
        n = get(row, f"OBJNAME_{cat}")
        if n:
            return n

    return None

