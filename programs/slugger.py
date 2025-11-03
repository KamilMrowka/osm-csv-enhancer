from dataclasses import dataclass
from slugify import slugify
from geo_csv import GeoNode
from typing import Set, cast

@dataclass
class Slug:
    slug_en: str
    slug_pl: str
    slug_ru: str
    slug_uk: str


def slugifyStreet(street: GeoNode, streetSlugs: Set[str]) -> str:
    base_slug = slugify(f"{street.name_primary}-{street.city_name}")
    slug = base_slug
    
    if slug in streetSlugs and street.district_name:
        slug = slugify(f"{street.name_primary}-{street.district_name}-{street.city_name}")
    
    if slug in streetSlugs:
        counter = 2
        base = slug
        while slug in streetSlugs:
            slug = f"{base}-{counter}"
            counter += 1
    
    streetSlugs.add(slug)
    return slug

def slugifyCity(city: GeoNode) -> str:
    return slugify(cast(str, city.name_primary))

def slugifyDistrict(district: GeoNode, districtSlugs: Set[str]) -> str:
    base_slug = slugify(f"{district.name_primary}-{district.city_name}")
    slug = base_slug
    counter = 2
    
    while slug in districtSlugs:
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    districtSlugs.add(slug)
    return slug

def slugifyNeighbourhood(neighbourhood: GeoNode, neighbourhoodSlugs: Set[str]) -> str:
    base_slug = slugify(f"{neighbourhood.name_primary}-{neighbourhood.city_name}")
    slug = base_slug
    
    if slug in neighbourhoodSlugs and neighbourhood.district_name:
        slug = slugify(f"{neighbourhood.name_primary}-{neighbourhood.district_name}-{neighbourhood.city_name}")
    
    if slug in neighbourhoodSlugs:
        counter = 2
        base = slug
        while slug in neighbourhoodSlugs:
            slug = f"{base}-{counter}"
            counter += 1
    
    neighbourhoodSlugs.add(slug)
    return slug
