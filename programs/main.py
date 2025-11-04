import sys
from geo_csv import read_geo_csv, merge_streets, write_geo_csv
from translator import translate
from slugger import slugifyCities, slugifyDistricts, slugifyNeighbourhoods, slugifyStreets

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
    print("Translated, adding slugs")

    slugifyStreets(collapsed_streets)
    slugifyCities(cities)
    slugifyDistricts(districts)
    slugifyNeighbourhoods(neighbourhoods)

    print("Slugs added, saving csv")

    write_geo_csv(
        nodes_by_type={
            "streets": collapsed_streets, 
            "cities": cities, 
            "districts": districts, 
            "neighbourhoods": neighbourhoods
        }, 
        file_path=getSaveDataPath()
    )
    print(f"Results saved to: {getSaveDataPath()}")

def getDataPath():
    actual_path = "data/updated_geo.csv"
    test_path = "data/updated_tiny.csv"
    return actual_path if isFullExport() else test_path

def getSaveDataPath():
    actual_path = "data/results/geo_out.csv"
    test_path = "data/results/tiny_out.csv"
    return actual_path if isFullExport() else test_path


def isFullExport():
    full_export = False
    
    if (len(sys.argv) > 1 and sys.argv[1] == "full"):
        full_export = True

    return full_export


main()
