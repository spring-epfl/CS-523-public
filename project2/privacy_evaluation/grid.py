import bisect

## Grid parameters
# Top left corner of the area
MAP_LAT = 46.5
MAP_LON = 6.55

# Total area size
MAP_SIZE_LAT = 0.07
MAP_SIZE_LON = 0.10

# Number of cells
CELL_NUM_LAT = 10
CELL_NUM_LON = 10

# Grid lines
GRID_LAT_POINTS = [MAP_LAT + i * (MAP_SIZE_LAT / CELL_NUM_LAT)
                   for i in range(1, CELL_NUM_LAT + 1)]
GRID_LON_POINTS = [MAP_LON + i * (MAP_SIZE_LON / CELL_NUM_LON)
                   for i in range(1, CELL_NUM_LON + 1)]


def location_to_cell_id(lat, lon):
    """Get the grid cell ID for a given latitude and longitude."""
    if not (MAP_LAT <= lat < MAP_LAT + MAP_SIZE_LAT) or not (
        MAP_LON <= lon < MAP_LON + MAP_SIZE_LON
    ):
        raise ValueError("Out of area range.")

    i = bisect.bisect(GRID_LAT_POINTS, lat)
    j = bisect.bisect(GRID_LON_POINTS, lon)
    return i * CELL_NUM_LAT + j + 1

