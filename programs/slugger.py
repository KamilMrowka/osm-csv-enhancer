from slugify import slugify
from geo_csv import GeoNode
from typing import Set, Dict, Optional, List

def _generate_slug_for_language(
    name: Optional[str],
    city_name: Optional[str],
    district_name: Optional[str],
    neighbourhood_name: Optional[str],
    slug_tracker: Set[str]
) -> str:
    if not name:
        name = "unnamed"
    if not city_name:
        city_name = "unknown"
    
    slug = slugify(f"{city_name}-{name}")

    if slug in slug_tracker and neighbourhood_name:
            slug = slugify(f"{city_name}-{name}-{neighbourhood_name}")
     
    if slug in slug_tracker and district_name:
        slug = slugify(f"{city_name}-{name}-{district_name}")
  
    if slug in slug_tracker:
        counter = 2
        base = slug
        while slug in slug_tracker:
            slug = f"{base}-{counter}"
            counter += 1
    
    slug_tracker.add(slug)
    return slug


def slugifyStreets(streets: List[GeoNode]) -> None:
    slug_trackers: Dict[str, Set[str]] = {
        'pl': set(),
        'en': set(),
        'ru': set(),
        'uk': set()
    }
    
    for street in streets:
        street.slug_pl = _generate_slug_for_language(
            street.name_pl,
            street.city_name_pl,
            street.district_name_pl,
            street.neighbourhood_name_pl,
            slug_trackers['pl']
        )
        
        street.slug_en = _generate_slug_for_language(
            street.name_en,
            street.city_name_en,
            street.district_name_en,
            street.neighbourhood_name_en,
            slug_trackers['en']
        )
        
        street.slug_ru = _generate_slug_for_language(
            street.name_ru,
            street.city_name_ru,
            street.district_name_ru,
            street.neighbourhood_name_ru,
            slug_trackers['ru']
        )
        
        street.slug_uk = _generate_slug_for_language(
            street.name_uk,
            street.city_name_uk,
            street.district_name_uk,
            street.neighbourhood_name_uk,
            slug_trackers['uk']
        )

def slugifyCities(cities: List[GeoNode]) -> None:
    slug_trackers: Dict[str, Set[str]] = {
        'pl': set(),
        'en': set(),
        'ru': set(),
        'uk': set()
    }
    
    for city in cities:
        slug_pl = slugify(city.name_pl or "unnamed")
        slug_en = slugify(city.name_en or "unnamed")
        slug_ru = slugify(city.name_ru or "unnamed")
        slug_uk = slugify(city.name_uk or "unnamed")
        
        city.slug_pl = _ensure_unique_slug(slug_pl, slug_trackers['pl'])
        city.slug_en = _ensure_unique_slug(slug_en, slug_trackers['en'])
        city.slug_ru = _ensure_unique_slug(slug_ru, slug_trackers['ru'])
        city.slug_uk = _ensure_unique_slug(slug_uk, slug_trackers['uk'])


def slugifyDistricts(districts: List[GeoNode]) -> None:
    slug_trackers: Dict[str, Set[str]] = {
        'pl': set(),
        'en': set(),
        'ru': set(),
        'uk': set()
    }
    
    for district in districts:
        slug_pl = slugify(f"{district.city_name_pl or 'unknown'}-{district.name_pl or 'unnamed'}")
        slug_en = slugify(f"{district.city_name_en or 'unknown'}-{district.name_en or 'unnamed'}")
        slug_ru = slugify(f"{district.city_name_ru or 'unknown'}-{district.name_ru or 'unnamed'}")
        slug_uk = slugify(f"{district.city_name_uk or 'unknown'}-{district.name_uk or 'unnamed'}")
        
        district.slug_pl = _ensure_unique_slug(slug_pl, slug_trackers['pl'])
        district.slug_en = _ensure_unique_slug(slug_en, slug_trackers['en'])
        district.slug_ru = _ensure_unique_slug(slug_ru, slug_trackers['ru'])
        district.slug_uk = _ensure_unique_slug(slug_uk, slug_trackers['uk'])


def slugifyNeighbourhoods(neighbourhoods: List[GeoNode]) -> None:
    slug_trackers: Dict[str, Set[str]] = {
        'pl': set(),
        'en': set(),
        'ru': set(),
        'uk': set()
    }
    
    for neighbourhood in neighbourhoods:
        slug_pl = slugify(f"{neighbourhood.city_name_pl or 'unknown'}-{neighbourhood.name_pl or 'unnamed'}")
        slug_en = slugify(f"{neighbourhood.city_name_en or 'unknown'}-{neighbourhood.name_en or 'unnamed'}")
        slug_ru = slugify(f"{neighbourhood.city_name_ru or 'unknown'}-{neighbourhood.name_ru or 'unnamed'}")
        slug_uk = slugify(f"{neighbourhood.city_name_uk or 'unknown'}-{neighbourhood.name_uk or 'unnamed'}")
        
        neighbourhood.slug_pl = _ensure_unique_slug(slug_pl, slug_trackers['pl'])
        neighbourhood.slug_en = _ensure_unique_slug(slug_en, slug_trackers['en'])
        neighbourhood.slug_ru = _ensure_unique_slug(slug_ru, slug_trackers['ru'])
        neighbourhood.slug_uk = _ensure_unique_slug(slug_uk, slug_trackers['uk'])


def _ensure_unique_slug(slug: str, slug_tracker: Set[str]) -> str:
    if slug not in slug_tracker:
        slug_tracker.add(slug)
        return slug
    
    counter = 2
    base = slug
    while slug in slug_tracker:
        slug = f"{base}-{counter}"
        counter += 1
    
    slug_tracker.add(slug)
    return slug

