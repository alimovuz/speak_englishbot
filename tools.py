import requests
from googletrans import Translator
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import os
translator = Translator()

load_dotenv()

URL = os.getenv("BASE_URL")
APP_KEY = os.getenv("API_KEY")
APP_ID = os.getenv("API_ID")

def deep_find(data, key):
    results = []

    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                results.append(v)
            elif isinstance(v, (dict, list)):
                results.extend(deep_find(v, key))

    elif isinstance(data, list):
        for item in data:
            results.extend(deep_find(item, key))

    return results


async def identify_lang(text):
    return await translator.detect(text)


def custom_translator(text, lang):
        translated = GoogleTranslator(source="auto", target=lang).translate(text)
        return translated


def get_word_details(word):
    res = requests.get(f"{URL}/en-gb/{word}", headers={"app_id": APP_ID, "app_key": APP_KEY})
    definitions = deep_find(res.json()["results"], "definitions")
    short_definitions = deep_find(res.json()["results"], "shortDefinitions")
    all_definitions = [elem for sublist in definitions for elem in sublist] + [elem for sublist in short_definitions for elem in sublist]
    return all_definitions