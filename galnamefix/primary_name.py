from astropy.coordinates import SkyCoord
import astropy.units as u

PREFIX_PRIORITY = ["NGC","IC","PGC","UGC","ESO","MCG","MRK","VCC","LEDA"]

def get(row, key):
    return row[key] if isinstance(row, dict) else getattr(row, key, None)

def get_prefix(name):
    if not name:
        return None
    return name.split()[0].upper()

def choose_primary(row, max_sep=10):
    catalogs = []
    for key in row.keys() if isinstance(row, dict) else row.__dict__.keys():
        if key.startswith("OBJNAME_"):
            catalogs.append(key.replace("OBJNAME_", ""))
    catalogs = sorted(set(catalogs))
    if not catalogs:
        return None

    coords = {}
    for cat in catalogs:
        ra, dec = get(row, f"RA_{cat}"), get(row, f"DEC_{cat}")
        if ra is not None and dec is not None:
            coords[cat] = SkyCoord(ra*u.deg, dec*u.deg)
    if len(coords) < 2:
        for cat in catalogs:
            n = get(row, f"OBJNAME_{cat}")
            if n:
                return n
        return None

    consistent = set()
    cat_list = list(coords.keys())
    for i in range(len(cat_list)):
        for j in range(i+1, len(cat_list)):
            a, b = cat_list[i], cat_list[j]
            if coords[a].separation(coords[b]).arcsec < max_sep:
                consistent.add(a)
                consistent.add(b)

    if consistent:
        cons_names = [get(row, f"OBJNAME_{cat}") for cat in consistent]
        for pref in PREFIX_PRIORITY:
            for name in cons_names:
                if name and get_prefix(name) == pref:
                    return name
        for cat in catalogs:
            if cat in consistent:
                n = get(row, f"OBJNAME_{cat}")
                if n:
                    return n

    for cat in catalogs:
        n = get(row, f"OBJNAME_{cat}")
        if n:
            return n
    return None

