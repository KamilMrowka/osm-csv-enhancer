import csv

# Columns to rename: old_name -> new_name
rename_map = {
    "name_primary": "name_pl",
    "name_ua": "name_uk",
    "city_name": "city_name_pl",
    "district_name": "district_name_pl",
    "neighbourhood_name": "neighbourhood_name_pl"
}

# Language variants to add (empty initially) for certain groups
lang_variants = {
    "name": ["name_pl", "name_en", "name_ru", "name_uk"],
    "city_name": ["city_name_pl", "city_name_en", "city_name_ru", "city_name_uk"],
    "district_name": ["district_name_pl", "district_name_en", "district_name_ru", "district_name_uk"],
    "neighbourhood_name": ["neighbourhood_name_pl", "neighbourhood_name_en", "neighbourhood_name_ru", "neighbourhood_name_uk"],
    "slug": ["slug_pl", "slug_en", "slug_ru", "slug_uk"]
}

with open("data/geospacial.csv", "r", newline="", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    old_header = reader.fieldnames
    if old_header is None:
        raise ValueError("CSV has no header row!")

    # Build new header in desired order
    new_header = [
        "osm_type", "osm_id", "kind",
        *lang_variants["name"],
        *lang_variants["slug"],
        *lang_variants["city_name"],
        *lang_variants["district_name"],
        *lang_variants["neighbourhood_name"],
        "geom", "bbox", "raw"
    ]

with open("data/geospacial.csv", "r", newline="", encoding="utf-8") as infile, \
     open("data/updated_geo.csv", "w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=new_header)
    writer.writeheader()

    for row in reader:
        new_row = {}
        # Copy old values to renamed columns if present
        for old_col, new_col in rename_map.items():
            if old_col in row:
                new_row[new_col] = row[old_col]

        # Copy unchanged columns
        for col in ["osm_type", "osm_id", "kind", "geom", "bbox", "raw"]:
            if col in row:
                new_row[col] = row[col]

        # Ensure all language and slug columns exist
        for group in lang_variants.values():
            for col in group:
                if col not in new_row:
                    new_row[col] = ""

        writer.writerow(new_row)

print("CSV updated successfully.")

