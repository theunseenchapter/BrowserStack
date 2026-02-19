import os
from dotenv import load_dotenv

load_dotenv()

# browserstack credentials
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
BROWSERSTACK_URL = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# rapidapi google translate
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "google-translate113.p.rapidapi.com"
TRANSLATE_URL = "https://google-translate113.p.rapidapi.com/api/v1/translator/json"

# el pais stuff
OPINION_URL = "https://elpais.com/opinion/"
NUM_ARTICLES = 5
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "downloaded_images")

# browser configs for browserstack - 3 desktop + 2 mobile
BROWSERS = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "Chrome Win11",
        }
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "sessionName": "Firefox Win10",
        }
    },
    {
        "browserName": "Safari",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "OS X",
            "osVersion": "Ventura",
            "sessionName": "Safari macOS",
        }
    },
    {
        "browserName": "Safari",
        "bstack:options": {
            "deviceName": "iPhone 15",
            "osVersion": "17",
            "sessionName": "iPhone 15",
        }
    },
    {
        "browserName": "Chrome",
        "bstack:options": {
            "deviceName": "Samsung Galaxy S23",
            "osVersion": "13.0",
            "sessionName": "Galaxy S23",
        }
    },
]
