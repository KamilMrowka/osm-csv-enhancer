import sys
from geo_csv import read_geo_csv, merge_streets


def main():
    nodes = read_geo_csv(getDataPath())

    streets = nodes["streets"]
    cities = nodes["cities"]
    neighbourhoods = nodes["neighbourhoods"]
    districts = nodes["districts"]

    collapsed_streets = merge_streets(streets)

    for street in streets:
        print("Street: ", f"{street.name_primary}-{street.district_name}-{street.city_name}")
    for district in districts:
        print("District: ", f"{district.name_primary}")
    for city in cities:
        print("City: ", f"{city.name_primary}")
    for neighbourhood in neighbourhoods:
        print("Neighbourhood: ", f"{neighbourhood.name_primary}")

    print("\n\n\n\n")
    for street in collapsed_streets:
        print("Street Collapsed: ", f"{street.name_primary}-{street.district_name}-{street.city_name}")


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
