# Runs the scraper on BrowserStack across 5 different browsers in parallel
# usage: python browserstack_runner.py

from concurrent.futures import ThreadPoolExecutor, as_completed
from modules.driver_factory import get_browserstack_driver
from modules.article_scraper import scrape_opinion_articles
from modules.translator import translate_titles
from modules.analysis import find_repeated_words, print_word_analysis
from config import BROWSERS


def run_test(caps):
    # runs the whole scraping flow on one browser
    name = caps.get("bstack:options", {}).get("sessionName", "Unknown")
    driver = None

    try:
        print(f"[{name}] Starting...")
        driver = get_browserstack_driver(caps)

        articles = scrape_opinion_articles(driver)
        print(f"[{name}] Got {len(articles)} articles")

        for i, art in enumerate(articles, 1):
            print(f"[{name}]   {i}. {art['title']}")

        eng_titles = translate_titles(articles)
        print(f"[{name}] Translated titles:")
        for i, art in enumerate(articles, 1):
            print(f"[{name}]   {i}. {art.get('title_en')}")

        repeated = find_repeated_words(eng_titles)

        # mark this session as passed on browserstack
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", '
            '"arguments": {"status": "passed", "reason": "All good"}}'
        )

        return {"name": name, "status": "passed", "repeated": repeated, "titles": eng_titles}

    except Exception as e:
        print(f"[{name}] FAILED - {e}")
        if driver:
            try:
                reason = str(e)[:250].replace('"', "'")
                driver.execute_script(
                    'browserstack_executor: {"action": "setSessionStatus", '
                    f'"arguments": {{"status": "failed", "reason": "{reason}"}}}}'
                )
            except:
                pass
        return {"name": name, "status": "failed", "error": str(e)}

    finally:
        if driver:
            driver.quit()


def main():
    print(f"\n=== El Pais Scraper - BrowserStack ({len(BROWSERS)} browsers) ===\n")

    results = []

    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(run_test, b): b for b in BROWSERS}
        for future in as_completed(futures):
            results.append(future.result())

    # print summary
    print("\n--- Results ---")
    passed = 0
    for r in results:
        status = "PASS" if r["status"] == "passed" else "FAIL"
        print(f"  [{status}] {r['name']}")
        if r.get("error"):
            print(f"         {r['error'][:80]}")
        if r["status"] == "passed":
            passed += 1

    print(f"\n  {passed}/{len(results)} passed")

    # show the word analysis from whichever browser finished first
    for r in results:
        if r.get("repeated"):
            print_word_analysis(r["repeated"])
            break

    print("Check BrowserStack dashboard for full session details.")


if __name__ == "__main__":
    main()
