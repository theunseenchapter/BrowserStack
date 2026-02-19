# Run the scraper locally with Chrome
# usage: python scraper.py

from modules.driver_factory import get_local_driver
from modules.article_scraper import scrape_opinion_articles
from modules.translator import translate_titles
from modules.analysis import find_repeated_words, print_word_analysis


def main():
    driver = get_local_driver()

    try:
        print("\n=== El Pais Opinion Scraper (Local) ===\n")

        # scrape the opinion section
        print("[1] Scraping articles from Opinion section...")
        articles = scrape_opinion_articles(driver)

        # print what we got (still in spanish at this point)
        print("\n[2] Articles (Spanish):")
        for i, art in enumerate(articles, 1):
            print(f"\n  Article {i}: {art['title']}")
            print(f"  Content: {art['content'][:400]}...")
            if art["image_file"]:
                print(f"  Image saved to: {art['image_file']}")

        # translate the titles to english
        print("\n[3] Translating titles to English...")
        eng_titles = translate_titles(articles)

        print("\n  Translated headers:")
        for i, art in enumerate(articles, 1):
            print(f"    {i}. {art.get('title_en', art['title'])}")

        # check which words appear more than twice across all titles
        print("\n[4] Analyzing translated headers...")
        repeated = find_repeated_words(eng_titles)
        print_word_analysis(repeated)

    finally:
        driver.quit()
        print("Done - browser closed.")


if __name__ == "__main__":
    main()
