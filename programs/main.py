from geo_csv import GeoNode, collapse_street, read_geo_csv
import sys
from typing import Dict, List, cast
from shapely.wkt import loads


def main():
    nodes = read_geo_csv(getDataPath())

    streets = nodes["streets"]
    cities = nodes["cities"]
    neighbourhoods = nodes["neighbourhoods"]
    districts = nodes["districts"]
    collapsed_streets = merge_streets(streets)

    for street in streets:
        print("Street: ", street.name_primary)
    for street in collapsed_streets:
        print("Street Collapsed: ", street.name_primary)

def merge_streets(streets: List[GeoNode]) -> List[GeoNode]:
    merged:List[GeoNode] = []
    by_city = merge_streets_by_city(streets)

    for s in by_city:
        city_streets = by_city[s]
        merged_city_streets = merge_streets_by_distance(city_streets)
        for merged_street in merged_city_streets:
            merged.append(merged_street)

    return merged


def merge_streets_by_city(streets: List[GeoNode]):
    streets_sorted: Dict[str, List[GeoNode]] = {}

    for street in streets:
        street_id = f"{street.name_primary}-{street.city_name}"

        if street_id not in streets_sorted:
            streets_sorted[street_id] = [street]
        else:
            streets_sorted[street_id].append(street)
    return streets_sorted


def merge_streets_by_distance(streets: List[GeoNode]) -> List[GeoNode]:
    unmerged: List[GeoNode] = [u for u in streets if u.geom is not None]
    merged: List[GeoNode] = []

    while (len(unmerged) > 0):
        print("WHILE HIGHER")
        base = unmerged[0]

        if (len(unmerged) == 1):
            unmerged.remove(base)
            merged.append(base)
            break

        currently_merged: GeoNode = base
        current_geom = loads(cast(str, currently_merged.geom))
        
        while True:
            print("WHILE LOWER")
            currently_merging: List[GeoNode] = []
            merged_anything = False

            for u in unmerged[1:]:
                geom = loads(cast(str, u.geom))
                if current_geom.distance(geom) < 0.005:
                    currently_merged = collapse_street([currently_merged, u])
                    current_geom = loads(cast(str, currently_merged.geom))
                    currently_merging.append(u)
                    merged_anything = True

            for s in currently_merging:
                unmerged.remove(s)

            if (not merged_anything):
                merged.append(currently_merged)
                break
            
        unmerged.remove(base)

    return merged


def getDataPath():
    actual_path = "data/geospacial.csv"
    test_path = "data/tinyspacial.csv"
    return actual_path if isFullExport() else test_path


def isFullExport():
    full_export = False
    
    if (len(sys.argv) > 1 and sys.argv[1] == "full"):
        full_export = True

    return full_export


main()
