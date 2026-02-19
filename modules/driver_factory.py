import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.options import ArgOptions

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_local_driver():
    # just starts chrome locally
    opts = ChromeOptions()
    opts.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(10)
    return driver


def get_browserstack_driver(caps):
    # connects to browserstack and gives back a remote webdriver
    from config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY, BROWSERSTACK_URL

    bstack_opts = caps.get("bstack:options", {})
    bstack_opts["userName"] = BROWSERSTACK_USERNAME
    bstack_opts["accessKey"] = BROWSERSTACK_ACCESS_KEY
    bstack_opts["projectName"] = "El Pais Scraper"
    bstack_opts["buildName"] = "Opinion Section Analysis"

    # ArgOptions works for any browser (chrome, firefox, safari..)
    # unlike ChromeOptions which is chrome-specific
    options = ArgOptions()
    for key, val in caps.items():
        if key == "bstack:options":
            options.set_capability(key, bstack_opts)
        else:
            options.set_capability(key, val)

    driver = webdriver.Remote(command_executor=BROWSERSTACK_URL, options=options)
    driver.implicitly_wait(10)
    return driver
