from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, cast
import csv
import os
from shapely import wkt
from shapely.geometry import MultiLineString
import copy
from shapely.wkt import loads


@dataclass
class GeoNode:
    osm_type: Optional[str]
    osm_id: Optional[str]
    kind: Optional[str]
    name_primary: Optional[str]
    name_en: Optional[str]
    name_ru: Optional[str]
    name_ua: Optional[str]
    slug_pl: Optional[str]
    slug_en: Optional[str]
    slug_ru: Optional[str]
    slug_ua: Optional[str]
    name_norm: Optional[str]
    city_name: Optional[str]
    district_name: Optional[str]
    neighbourhood_name: Optional[str]
    geom: Optional[str]
    bbox: Optional[str]
    raw: Optional[str]

def read_geo_csv(file_path: str) -> Dict[str, List[GeoNode]]:
    result = {
         "streets": [],
         "neighbourhoods": [],
         "cities": [],
         "districts": []
    }

    if not os.path.exists(file_path):
        return result
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            node = GeoNode(
                osm_type=row.get('osm_type'),
                osm_id=row.get('osm_id'),
                kind=row.get('kind'),
                name_primary=row.get('name_primary'),
                name_en=row.get('name_en'),
                name_ru=row.get('name_ru'),
                name_ua=row.get('name_ua'),
                slug_pl=row.get('slug_pl'),
                slug_en=row.get('slug_en'),
                slug_ru=row.get('slug_ru'),
                slug_ua=row.get('slug_ua'),
                name_norm=row.get('name_norm'),
                city_name=row.get('city_name'),
                district_name=row.get('district_name'),
                neighbourhood_name=row.get('neighbourhood_name'),
                geom=row.get('geom'),
                bbox=row.get('bbox'),
                raw=row.get('raw')
            )

            kind = row.get("kind")
            if kind == "street":
                result["streets"].append(node)
            elif kind == "neighbourhood":
                result["neighbourhoods"].append(node)
            elif kind == "city":
                result["cities"].append(node)
            elif kind == "district":
                result["districts"].append(node)
    return result

from dataclasses import asdict
import os
import csv
from typing import List, Dict

def write_geo_csv(
    nodes_by_type: Dict[str, List[GeoNode]], 
    file_path: str, 
    overwrite: bool = False
):
    nodes: List[GeoNode] = []
    for lst in nodes_by_type.values():
        nodes.extend(lst)

    fieldnames = [f.name for f in GeoNode.__dataclass_fields__.values()]

    existing_nodes = {}
    if not overwrite and os.path.exists(file_path):
        existing_nodes_flat = read_geo_csv(file_path)
        for lst in existing_nodes_flat.values():
            for node in lst:
                if node.osm_id:
                    existing_nodes[node.osm_id] = node

    for node in nodes:
        if node.osm_id:
            existing_nodes[node.osm_id] = node

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for node in existing_nodes.values():
            writer.writerow(asdict(node))


def collapse_street(streets: List[GeoNode]):
    line_strings: List[str] = []
    multi_line_strings: List[str] = []
    if (len(streets) < 1):
        raise Exception("Cannot collapse an empty list")

    for street in streets:
        if (street.geom is None):
            continue
        if (wkt.loads(street.geom).geom_type == "LineString"):
            line_strings.append(street.geom)
        elif(wkt.loads(street.geom).geom_type == "MultiLineString"):
            multi_line_strings.append(street.geom)
        else:
            continue

    all_coords = []

    for line in line_strings:
        all_coords.append(wkt.loads(line).coords)

    for multi_wkt in multi_line_strings:
        multi = wkt.loads(multi_wkt)
        if isinstance(multi, MultiLineString):
            for line in multi.geoms:
                all_coords.append(line.coords)

    multi_line_string = MultiLineString(all_coords)
    collapsed_street = copy.copy(streets[0]) 
    collapsed_street.geom = multi_line_string.wkt

    return collapsed_street

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
