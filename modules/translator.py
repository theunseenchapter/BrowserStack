import sys
import os
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RAPIDAPI_KEY, RAPIDAPI_HOST, TRANSLATE_URL


def translate(text, from_lang="auto", to_lang="en"):
    # calls the google translate api through rapidapi
    resp = requests.post(
        TRANSLATE_URL,
        json={"from": from_lang, "to": to_lang, "json": {"text": text}},
        headers={
            "Content-Type": "application/json",
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST,
        },
        timeout=10
    )
    resp.raise_for_status()
    data = resp.json()

    # the /json endpoint can return either {"trans": {"text": "..."}} or {"trans": "..."}
    # so we handle both cases
    trans = data.get("trans", text)
    if isinstance(trans, dict):
        return trans.get("text", text)
    return trans


def translate_titles(articles):
    # takes a list of articles and translates each title from spanish to english
    translated = []
    for art in articles:
        try:
            eng = translate(art["title"])
            art["title_en"] = eng
            translated.append(eng)
            print(f"  '{art['title']}' -> '{eng}'")
        except Exception as e:
            print(f"  Translation failed for '{art['title']}': {e}")
            art["title_en"] = art["title"]  # fallback to spanish
            translated.append(art["title"])
    return translated
