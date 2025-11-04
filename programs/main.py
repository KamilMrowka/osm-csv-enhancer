import sys
from geo_csv import read_geo_csv, merge_streets, write_geo_csv
from translator import translate

def main():
    nodes = read_geo_csv(getDataPath())

    streets = nodes["streets"]
    cities = nodes["cities"]
    neighbourhoods = nodes["neighbourhoods"]
    districts = nodes["districts"]

    collapsed_streets = merge_streets(streets)
    print("Streets collapsed")

    print("translating")
    translate(cities, districts, neighbourhoods, collapsed_streets)
    print("Translated")

    for city in cities:
        print("City-PL: ", f"{city.name_pl}")
        print("City-EN: ", f"{city.name_en}")
        print("City-RU: ", f"{city.name_ru}")
        print("City-UK: ", f"{city.name_uk}")
        print("\n\n\n\n")

    for street in collapsed_streets:
        print("Street-PL: ", f"{street.name_pl}-{street.district_name_pl}-{street.city_name_pl}-{street.neighbourhood_name_pl}")
        print("Street-EN: ", f"{street.name_en}-{street.district_name_en}-{street.city_name_en}-{street.neighbourhood_name_en}")
        print("Street-RU: ", f"{street.name_ru}-{street.district_name_ru}-{street.city_name_ru}-{street.neighbourhood_name_ru}")
        print("Street-UK: ", f"{street.name_uk}-{street.district_name_uk}-{street.city_name_uk}-{street.neighbourhood_name_uk}")
        print("\n\n\n\n")

    for district in districts:
        print("Disctrict-PL: ", f"{district.name_pl}-{district.city_name_pl}")
        print("Disctrict-EN: ", f"{district.name_en}-{district.city_name_en}")
        print("Disctrict-RU: ", f"{district.name_ru}-{district.city_name_ru}")
        print("Disctrict-UK: ", f"{district.name_uk}-{district.city_name_uk}")
        print("\n\n\n\n")

    for neighbourhood in neighbourhoods:
        print("neighbourhood-PL: ", f"{neighbourhood.district_name_pl}-{neighbourhood.city_name_pl}")
        print("neighbourhood-EN: ", f"{neighbourhood.district_name_en}-{neighbourhood.city_name_en}")
        print("neighbourhood-RU: ", f"{neighbourhood.district_name_ru}-{neighbourhood.city_name_ru}")
        print("neighbourhood-UK: ", f"{neighbourhood.district_name_uk}-{neighbourhood.city_name_uk}")
        print("\n\n\n\n")

    write_geo_csv(nodes_by_type={"streets": collapsed_streets, "cities": cities, "districts": districts, "neighbourhoods": neighbourhoods}, file_path="data/results/tiny_out.csv")

def getDataPath():
    actual_path = "data/updated_geo.csv"
    test_path = "data/updated_tiny.csv"
    return actual_path if isFullExport() else test_path

def isFullExport():
    full_export = False
    
    if (len(sys.argv) > 1 and sys.argv[1] == "full"):
        full_export = True

    return full_export


main()
