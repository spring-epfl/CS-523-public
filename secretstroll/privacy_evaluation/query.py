import numpy as np
from os import path

# Globals
DIST_THRESH = 0.01


def load_poi_data():
    cwd = path.dirname(__file__)
    dat = np.loadtxt(path.join(cwd, 'pois.csv'), delimiter=" ", dtype=object, skiprows=1)
    poi_ids = dat[:, 0].astype(int)
    poi_type = dat[:, 2]
    poi_loc = dat[:, -2:].astype(float)

    return poi_ids, poi_type, poi_loc


POI_IDS, POI_TYPES, POI_LOCS = load_poi_data()


def get_nearby_pois(loc: np.ndarray, poi_type: str):
    """ Find nearby POIs of the specified type """
    poi_ids = []

    for i, poi_loc in enumerate(POI_LOCS):
        if POI_TYPES[i] == poi_type:
            d = np.linalg.norm(loc - poi_loc)

            if d <= DIST_THRESH:
                poi_ids.append(POI_IDS[i])

    return poi_ids

