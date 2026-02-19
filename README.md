# El Pais Opinion Scraper

A Selenium-based scraper that pulls articles from the Opinion section of [El País](https://elpais.com/opinion/), translates the titles to English, and does some basic word frequency analysis on them.

## What it does

1. Opens El País and confirms the page is in Spanish
2. Scrapes the first 5 opinion articles (title, content, cover image)
3. Translates article titles from Spanish to English using the Google Translate API (via RapidAPI)
4. Checks which words appear more than twice across all the translated titles
5. Can run locally on Chrome or across 5 browsers in parallel on BrowserStack

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`):

```
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
RAPIDAPI_KEY=your_rapidapi_key
```

## Running

Local (Chrome):
```bash
python scraper.py
```

BrowserStack (5 browsers in parallel):
```bash
python browserstack_runner.py
```

## Project Structure

```
scraper.py                  - local runner
browserstack_runner.py      - browserstack parallel runner
config.py                   - credentials and browser configs
modules/
    article_scraper.py      - scraping logic
    translator.py           - translation via rapidapi
    analysis.py             - word frequency stuff
    driver_factory.py       - creates local/remote webdrivers
```

## Browsers tested on BrowserStack

- Chrome (Windows 11)
- Firefox (Windows 10)
- Safari (macOS Ventura)
- iPhone 15
- Samsung Galaxy S23
