import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.simbad import Simbad
from astroquery.ned import Ned
from astroquery.sdss import SDSS

Simbad.add_votable_fields('otype')

def query_simbad_improved(ra, dec, radius_arcsec=15):
    try:
        pos = SkyCoord(ra*u.deg, dec*u.deg)
        result = Simbad.query_region(pos, radius=radius_arcsec*u.arcsec)
        if result is None or len(result) == 0:
            return None, None, None
        row = result[0]
        name = row['MAIN_ID']
        if isinstance(name, bytes):
            name = name.decode('utf-8')
        ra_deg = SkyCoord(row['RA'], row['DEC'], unit=(u.hourangle, u.deg)).ra.deg
        dec_deg = SkyCoord(row['RA'], row['DEC'], unit=(u.hourangle, u.deg)).dec.deg
        return name, ra_deg, dec_deg
    except Exception:
        return None, None, None

def query_ned(ra, dec, radius_arcsec=15):
    try:
        pos = SkyCoord(ra*u.deg, dec*u.deg)
        result = Ned.query_region(pos, radius=radius_arcsec*u.arcsec)
        if result is None or len(result) == 0:
            return None, None, None
        row = result[0]
        name = row['Object Name']
        return name, row['RA'], row['DEC']
    except Exception:
        return None, None, None

def query_sdss(ra, dec, radius_arcsec=5):
    try:
        pos = SkyCoord(ra*u.deg, dec*u.deg)
        xid = SDSS.query_region(pos, radius=radius_arcsec*u.arcsec, spectro=True)
        if xid is None or len(xid) == 0:
            return None, None, None
        row = xid[0]
        name = f"SDSS J{row['ra']:.5f}{row['dec']:+.5f}"
        return name, row['ra'], row['dec']
    except Exception:
        return None, None, None

def process_galaxy_catalog(csvfile, simbad_radius=15, ned_radius=15, sdss_radius=5):
    df = pd.read_csv(csvfile)
    df["OBJNAME_SIMBAD"], df["RA_SIMBAD"], df["DEC_SIMBAD"] = None, None, None
    df["OBJNAME_NED"], df["RA_NED"], df["DEC_NED"] = None, None, None
    df["OBJNAME_SDSS"], df["RA_SDSS"], df["DEC_SDSS"] = None, None, None

    for i, row in df.iterrows():
        ra, dec = row["_RA"], row["_DE"]

        s_name, s_ra, s_dec = query_simbad_improved(ra, dec, simbad_radius)
        n_name, n_ra, n_dec = query_ned(ra, dec, ned_radius)
        sdss_name, sdss_ra, sdss_dec = query_sdss(ra, dec, sdss_radius)

        df.loc[i, ["OBJNAME_SIMBAD","RA_SIMBAD","DEC_SIMBAD"]] = [s_name, s_ra, s_dec]
        df.loc[i, ["OBJNAME_NED","RA_NED","DEC_NED"]] = [n_name, n_ra, n_dec]
        df.loc[i, ["OBJNAME_SDSS","RA_SDSS","DEC_SDSS"]] = [sdss_name, sdss_ra, sdss_dec]

        print(f"Row {i}: SIMBAD={s_name}, NED={n_name}, SDSS={sdss_name}")

    return df

