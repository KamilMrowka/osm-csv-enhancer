from dataclasses import dataclass
from slugify import slugify
from geo_csv import GeoNode
from typing import List

@dataclass
class Slugs():
    slug_pl: str
    slug_en: str
    slug_ru: str
    slug_uk: str

used_pl = set()
used_en = set()
used_ru = set()
used_uk = set()

def slugifyStreets(streets: List[GeoNode]) -> None:
    for street in streets:
        slugs = generate_slug_for_street(street)
        addSlugsToUsed(slugs)

        street.slug_pl = slugs.slug_pl
        street.slug_en = slugs.slug_en
        street.slug_ru = slugs.slug_ru
        street.slug_uk = slugs.slug_uk

def slugifyCities(cities: List[GeoNode]) -> None:
    for city in cities:
        slugs = generate_slug_for_city(city)
        addSlugsToUsed(slugs)

        city.slug_pl = slugs.slug_pl
        city.slug_en = slugs.slug_en
        city.slug_ru = slugs.slug_ru
        city.slug_uk = slugs.slug_uk


def slugifyDistricts(districts: List[GeoNode]) -> None:
    for district in districts:
        slugs = generate_slug_for_district(district)
        addSlugsToUsed(slugs)

        district.slug_pl = slugs.slug_pl
        district.slug_en = slugs.slug_en
        district.slug_ru = slugs.slug_ru
        district.slug_uk = slugs.slug_uk

   
def slugifyNeighbourhoods(neighbourhoods: List[GeoNode]) -> None:
    for neighbourhood in neighbourhoods:
        slugs = generate_slug_for_neighbourhood(neighbourhood)
        addSlugsToUsed(slugs)

        neighbourhood.slug_pl = slugs.slug_pl
        neighbourhood.slug_en = slugs.slug_en
        neighbourhood.slug_ru = slugs.slug_ru
        neighbourhood.slug_uk = slugs.slug_uk


def generate_slug_for_street(street: GeoNode) -> Slugs:
    slugs = Slugs(
        slug_pl=(slugify(f"{street.city_name_pl}-{street.name_pl}")),
        slug_en=(slugify(f"{street.city_name_en}-{street.name_en}")),
        slug_ru=(slugify(f"{street.city_name_ru}-{street.name_ru}")),
        slug_uk=(slugify(f"{street.city_name_uk}-{street.name_uk}"))
    )

    if (slugs.slug_pl in used_pl or slugs.slug_en in used_en or slugs.slug_ru in used_ru or slugs.slug_uk in used_uk):
        slugs = Slugs(
            slug_pl=(slugify(f"{street.city_name_pl}-{street.name_pl}-{street.neighbourhood_name_pl}")),
            slug_en=(slugify(f"{street.city_name_en}-{street.name_en}-{street.neighbourhood_name_en}")),
            slug_ru=(slugify(f"{street.city_name_ru}-{street.name_ru}-{street.neighbourhood_name_ru}")),
            slug_uk=(slugify(f"{street.city_name_uk}-{street.name_uk}-{street.neighbourhood_name_uk}"))
        )

    counter = 2
    while (slugs.slug_pl in used_pl or slugs.slug_en in used_en or slugs.slug_ru in used_ru or slugs.slug_uk in used_uk):
        slugs = Slugs(
                slug_pl=(slugify(f"{street.city_name_pl}-{street.name_pl}-{street.neighbourhood_name_pl}-{counter}")),
                slug_en=(slugify(f"{street.city_name_en}-{street.name_en}-{street.neighbourhood_name_en}-{counter}")),
                slug_ru=(slugify(f"{street.city_name_ru}-{street.name_ru}-{street.neighbourhood_name_ru}-{counter}")),
                slug_uk=(slugify(f"{street.city_name_uk}-{street.name_uk}-{street.neighbourhood_name_uk}-{counter}"))
        )
        counter += 1

    return slugs


def generate_slug_for_city(city: GeoNode) -> Slugs:
    slugs = Slugs(
        slug_pl=(slugify(f"{city.name_pl}")),
        slug_en=(slugify(f"{city.name_en}")),
        slug_ru=(slugify(f"{city.name_ru}")),
        slug_uk=(slugify(f"{city.name_uk}"))
    )

    return slugs


def generate_slug_for_district(district: GeoNode) -> Slugs:
    slugs = Slugs(
        slug_pl=(slugify(f"{district.city_name_pl}-{district.name_pl}")),
        slug_en=(slugify(f"{district.city_name_en}-{district.name_en}")),
        slug_ru=(slugify(f"{district.city_name_ru}-{district.name_ru}")),
        slug_uk=(slugify(f"{district.city_name_uk}-{district.name_uk}"))
    )

    counter = 2
    while (slugs.slug_pl in used_pl or slugs.slug_en in used_en or slugs.slug_ru in used_ru or slugs.slug_uk in used_uk):
        slugs = Slugs(
                slug_pl=(slugify(f"{district.city_name_pl}-{district.name_pl}-{counter}")),
                slug_en=(slugify(f"{district.city_name_en}-{district.name_en}-{counter}")),
                slug_ru=(slugify(f"{district.city_name_ru}-{district.name_ru}-{counter}")),
                slug_uk=(slugify(f"{district.city_name_uk}-{district.name_uk}-{counter}"))
        )
        counter += 1

    return slugs

def generate_slug_for_neighbourhood(neighbourhood: GeoNode) -> Slugs:
    slugs = Slugs(
        slug_pl=(slugify(f"{neighbourhood.city_name_pl}-{neighbourhood.name_pl}")),
        slug_en=(slugify(f"{neighbourhood.city_name_en}-{neighbourhood.name_en}")),
        slug_ru=(slugify(f"{neighbourhood.city_name_ru}-{neighbourhood.name_ru}")),
        slug_uk=(slugify(f"{neighbourhood.city_name_uk}-{neighbourhood.name_uk}"))
    )

    if (slugs.slug_pl in used_pl or slugs.slug_en in used_en or slugs.slug_ru in used_ru or slugs.slug_uk in used_uk):
        slugs = Slugs(
            slug_pl=(slugify(f"{neighbourhood.city_name_pl}-{neighbourhood.district_name_pl}-{neighbourhood.name_pl}")),
            slug_en=(slugify(f"{neighbourhood.city_name_en}-{neighbourhood.district_name_en}-{neighbourhood.name_en}")),
            slug_ru=(slugify(f"{neighbourhood.city_name_ru}-{neighbourhood.district_name_ru}-{neighbourhood.name_ru}")),
            slug_uk=(slugify(f"{neighbourhood.city_name_uk}-{neighbourhood.district_name_uk}-{neighbourhood.name_uk}"))
        )

    counter = 2
    while (slugs.slug_pl in used_pl or slugs.slug_en in used_en or slugs.slug_ru in used_ru or slugs.slug_uk in used_uk):
        slugs = Slugs(
                slug_pl=(slugify(f"{neighbourhood.city_name_pl}-{neighbourhood.district_name_pl}-{neighbourhood.name_pl}-{counter}")),
                slug_en=(slugify(f"{neighbourhood.city_name_en}-{neighbourhood.district_name_en}-{neighbourhood.name_en}-{counter}")),
                slug_ru=(slugify(f"{neighbourhood.city_name_ru}-{neighbourhood.district_name_ru}-{neighbourhood.name_ru}-{counter}")),
                slug_uk=(slugify(f"{neighbourhood.city_name_uk}-{neighbourhood.district_name_uk}-{neighbourhood.name_uk}-{counter}"))
        )
        counter += 1

    return slugs

def addSlugsToUsed(slugs :Slugs):
    used_pl.add(slugs.slug_pl)
    used_en.add(slugs.slug_en)
    used_ru.add(slugs.slug_ru)
    used_uk.add(slugs.slug_uk)

