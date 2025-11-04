from openai import OpenAI
from openai import OpenAI
from pydantic import BaseModel
from typing import Dict, List, Literal, cast
from geo_csv import GeoNode
from dotenv import load_dotenv
import os

Kind = Literal["city", "district", "neighbourhood", "street", "unknown"]

load_dotenv()
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

class GeoTranslation(BaseModel):
    name_pl: str
    name_en: str
    name_ru: str
    name_uk: str

class GptTranslationResponse(BaseModel):
    translations: List[GeoTranslation]

translatedCities: Dict[str, GeoTranslation] = {} 
translatedDistricts: Dict[str, GeoTranslation] = {} 
translatedNeighbourhoods: Dict[str, GeoTranslation] = {} 
translatedStreets: Dict[str, GeoTranslation] = {} 

translate_batch_size = 100
def getTranslationsDictionary(translations: List[GeoTranslation]):
    dictionary: Dict[str, GeoTranslation] = {}
    for translation in translations:
        dictionary[translation.name_pl] = translation
    return dictionary


def translate(cities: List[GeoNode], districts: List[GeoNode], neighbourhoods: List[GeoNode], streets: List[GeoNode]):
    print("Translating Started...")

    print("Translating Cities")
    city_translations = getOpenAITranslations(cities, "city").translations
    city_translations_dict = getTranslationsDictionary(city_translations)
    translatedCities.update(city_translations_dict)

    for city in cities:
        setTranslation(city, city_translations_dict[cast(str, city.name_pl)], "city")

    print("cities done, translating districts")
    # Translate Disctrics and add City Translation to them
    for i in range(0, len(districts), translate_batch_size):

        to_translate = districts[i:i+translate_batch_size]
        district_translations = getOpenAITranslations(to_translate, "district").translations
        district_translations_dict = getTranslationsDictionary(district_translations)
        translatedDistricts.update(district_translations_dict)

        for location in to_translate:
            district_translation = translatedDistricts[cast(str, location.name_pl)]
            setTranslation(location, district_translation, "district")
           
            city_name = location.city_name_pl
            if (city_name is not None):
                city_translation = findInAlreadyTranslated(city_name, "city")
                if (city_translation is None):
                    city_translation = getOpenAITranslation(city_name, "city")
                    translatedCities[city_name] = city_translation
                setTranslation(location, city_translation, "city")

    print("districts done, translating neighbourhoods")
    # Translate neighbourhoods and try to add city and district names from already translated
    for i in range(0, len(neighbourhoods), translate_batch_size):
        to_translate = neighbourhoods[i:i+translate_batch_size]
        neighbourhood_translations = getOpenAITranslations(to_translate, "neighbourhood").translations
        neighbourhood_translations_dict = getTranslationsDictionary(neighbourhood_translations)
        translatedNeighbourhoods.update(neighbourhood_translations_dict)

        for location in to_translate:
            neighbourhood_translation = neighbourhood_translations_dict[cast(str, location.name_pl)]
            setTranslation(location, neighbourhood_translation, "neighbourhood")
           
            city_name = location.city_name_pl
            if (city_name is not None):
                city_translation = findInAlreadyTranslated(city_name, "city")
                if (city_translation is None):
                    city_translation = getOpenAITranslation(city_name, "city")
                    translatedCities[city_name] = city_translation
                setTranslation(location, city_translation, "city")

            district_name = location.district_name_pl
            if (district_name is not None):
                district_translation = findInAlreadyTranslated(district_name, "district")
                if (district_translation is None):
                    district_translation = getOpenAITranslation(district_name, "district")
                    translatedDistricts[district_name] = district_translation
                setTranslation(location, district_translation, "district")

    print("neighbourhoods done, translating streets")
    # Translate Streets
    for i in range(0, len(streets), translate_batch_size):
        to_translate = streets[i:i+translate_batch_size]
        street_translations = getOpenAITranslations(to_translate, "street").translations
        street_translations_dict = getTranslationsDictionary(street_translations)
        translatedStreets.update(street_translations_dict)

        for location in to_translate:
            street_translation = street_translations_dict[cast(str, location.name_pl)]
            setTranslation(location, street_translation, "street")
           
            city_name = location.city_name_pl
            if (city_name is not None):
                city_translation = findInAlreadyTranslated(city_name, "city")
                if (city_translation is None):
                    city_translation = getOpenAITranslation(city_name, "city")
                    translatedCities[city_name] = city_translation
                setTranslation(location, city_translation, "city")

            district_name = location.district_name_pl
            if (district_name is not None):
                district_translation = findInAlreadyTranslated(district_name, "district")
                if (district_translation is None):
                    district_translation = getOpenAITranslation(district_name, "district")
                    translatedDistricts[district_name] = district_translation
                setTranslation(location, district_translation, "district")

            neighbourhood_name = location.neighbourhood_name_pl
            if (neighbourhood_name is not None):
                neighbourhood_translation = findInAlreadyTranslated(neighbourhood_name, "neighbourhood")
                if (neighbourhood_translation is None):
                    neighbourhood_translation = getOpenAITranslation(neighbourhood_name, "neighbourhood")
                    translatedNeighbourhoods[neighbourhood_name] = neighbourhood_translation
                setTranslation(location, neighbourhood_translation, "neighbourhood")

    print("done")


def getOpenAITranslation(location: str, kind: Kind) -> GeoTranslation:
    response = client.beta.chat.completions.parse(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": getTranslationSystemPrompt(True)},
        {"role": "user", "content": f"Location: '{location}'\nKind: {kind}"},
    ],
    response_format=GeoTranslation,
    reasoning_effort="minimal"
)
    translation = response.choices[0].message.parsed
    if translation is None:
        raise  Exception(f"Failed to translate {location}")

    return translation


def getOpenAITranslations(locations: List[GeoNode], kind: Kind) -> GptTranslationResponse:
    print(f"Translating {kind} kind with openai, amount: {len(locations)}")
    response = client.beta.chat.completions.parse(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": getTranslationSystemPrompt()},
            {"role": "user", "content": getTranslationUserPrompt(locations, kind)}
        ],
        response_format=GptTranslationResponse,
        reasoning_effort="minimal"
    )

    translation = response.choices[0].message.parsed

    if (translation is not None):
        print(f"Translated {kind} kind with openai, amount: {len(translation.translations)}")
    else:
        print(f"Failed to translat {kind} kind with openai, returned list is empty")
    if translation is None:
        raise  Exception(f"Failed to translate {len(locations)} locations.")

    return translation


def findInAlreadyTranslated(name_pl: str, kind: Kind) -> GeoTranslation | None:
    match kind:
        case "city":
            return translatedCities.get(name_pl)
        case "district":
            return translatedDistricts.get(name_pl)
        case "neighbourhood":
            return translatedNeighbourhoods.get(name_pl)
        case "street":
            return translatedStreets.get(name_pl)

def setTranslation(location: GeoNode, translation: GeoTranslation, kind: Kind):
    match kind:
        case "city":
            if (location.kind == "city"):
                location.name_en = translation.name_en
                location.name_ru = translation.name_ru
                location.name_uk = translation.name_uk
            else:
                location.city_name_en = translation.name_en
                location.city_name_ru = translation.name_ru
                location.city_name_uk = translation.name_uk

        case "district":
            if (location.kind == "district"):
                location.name_en = translation.name_en
                location.name_ru = translation.name_ru
                location.name_uk = translation.name_uk
            else:
                location.district_name_en = translation.name_en
                location.district_name_ru = translation.name_ru
                location.district_name_uk = translation.name_uk

        case "neighbourhood":
            if (location.kind == "neighbourhood"):
                location.name_en = translation.name_en
                location.name_ru = translation.name_ru
                location.name_uk = translation.name_uk
            else:
                location.neighbourhood_name_en = translation.name_en
                location.neighbourhood_name_ru = translation.name_ru
                location.neighbourhood_name_uk = translation.name_uk

        case "street":
            location.name_en = translation.name_en
            location.name_ru = translation.name_ru
            location.name_uk = translation.name_uk


def getTranslationSystemPrompt(single: bool = False) -> str:

    if single:
        return """
        You are a professional translator. Your task now is to translate location names from Poland to these target languages: English, Russian, Ukrainian.
        You will be given either a city, district, neighbourhood or a streets to translate.
        In the response give the translation for all three of the required languages. For empty location just return empty strings.
        """

    return """
    You are a professional translator. Your task now is to translate location names from Poland to these target languages: English, Russian, Ukrainian.
    You will be given a list of either Cities, Districts, neighbourhoods or Streets to translate. 
    All elements in the given list will be of the same kind and you will always be told what kind of locations you have to translate this time.
    In the response give the translation for all three of the required languages. For empty location just return empty strings.
    """


def getTranslationUserPrompt(locations: List[GeoNode], kind: Kind) -> str:
    string = f"Locations: {getLocationsPromptString(locations)}\nKind: {kind}"
    return string


def getLocationsPromptString(locations: List[GeoNode]) -> str:
    prompt_string = ""

    for location in locations:
        prompt_string += f"{location.name_pl}, " 

    return f"[{prompt_string[0:-2]}]"
