import os
import sys
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPINION_URL, NUM_ARTICLES, IMAGE_DIR


def handle_cookies(driver):
    # sometimes el pais shows a cookie popup (Didomi), just click accept if its there
    try:
        accept_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
        )
        accept_btn.click()
    except:
        pass


def check_spanish(driver):
    # verify the page language is spanish
    lang = driver.find_element(By.TAG_NAME, "html").get_attribute("lang")
    if lang and lang.startswith("es"):
        print(f"  Language confirmed: {lang}")
        return True
    print(f"  Warning: expected Spanish but got '{lang}'")
    return False


def get_article_content(driver, url):
    # opens an article page and tries to pull out the text + cover image
    driver.get(url)
    content = "(could not extract content)"
    image_url = None

    # get the article text
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
        )
        # el pais keeps changing their css classes so we try a few selectors
        selectors = [
            "article .a_b p",
            "article .article_body p",
            "article [data-dtm-region='articulo_cuerpo'] p",
            "article p"
        ]
        for sel in selectors:
            paragraphs = driver.find_elements(By.CSS_SELECTOR, sel)
            if paragraphs:
                text = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())
                if text:
                    content = text
                    break
    except Exception as e:
        print(f"    couldn't get article text: {e}")

    # now try to find the cover image
    try:
        time.sleep(2)  # wait a bit for lazy loaded images

        # on el pais the main image is usually inside figure > span.a_m_w > img
        img_selectors = [
            "figure span.a_m_w img",
            "figure img",
            "article figure img",
            "article header img"
        ]
        for sel in img_selectors:
            imgs = driver.find_elements(By.CSS_SELECTOR, sel)
            for img in imgs:
                src = img.get_attribute("src") or img.get_attribute("data-src") or ""
                w = img.get_attribute("width") or ""

                # skip tiny tracking pixels, svgs etc
                if not src or src.endswith(".svg") or "data:" in src:
                    continue
                if w and w.isdigit() and int(w) < 10:
                    continue

                image_url = src
                break
            if image_url:
                break

        if image_url:
            print(f"    Found cover image: {image_url[:80]}...")
        else:
            print(f"    No cover image found on this page")
    except Exception as e:
        print(f"    image extraction failed: {e}")

    return content, image_url


def save_image(url, idx):
    # downloads the image and saves it to the downloaded_images folder
    try:
        if url.startswith("//"):
            url = "https:" + url

        resp = requests.get(url, timeout=15)
        resp.raise_for_status()

        # figure out file extension from content-type
        ctype = resp.headers.get("Content-Type", "")
        if "png" in ctype:
            ext = "png"
        elif "webp" in ctype:
            ext = "webp"
        else:
            ext = "jpg"

        os.makedirs(IMAGE_DIR, exist_ok=True)
        filepath = os.path.join(IMAGE_DIR, f"article_{idx + 1}.{ext}")
        with open(filepath, "wb") as f:
            f.write(resp.content)
        print(f"  Saved image: article_{idx + 1}.{ext}")
        return filepath
    except Exception as e:
        print(f"  Could not download image: {e}")
        return None


def scrape_opinion_articles(driver):
    # main function - goes to opinion section, grabs first 5 articles,
    # fetches their content and downloads cover images

    print(f"  Opening {OPINION_URL}")
    driver.get(OPINION_URL)

    handle_cookies(driver)
    check_spanish(driver)

    # wait until we can see articles on the page
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article"))
    )

    all_articles = driver.find_elements(By.CSS_SELECTOR, "article")
    articles = []

    for el in all_articles:
        if len(articles) >= NUM_ARTICLES:
            break

        title = ""
        link = ""
        try:
            h2 = el.find_element(By.CSS_SELECTOR, "h2 a")
            title = h2.text.strip()
            link = h2.get_attribute("href")
        except:
            # some articles might not have a link in the h2
            try:
                title = el.find_element(By.TAG_NAME, "h2").text.strip()
            except:
                continue

        if not title:
            continue

        # check if theres an image on the listing page itself
        img_url = None
        try:
            img = el.find_element(By.CSS_SELECTOR, "figure img")
            img_url = img.get_attribute("src") or img.get_attribute("data-src")
        except:
            pass

        articles.append({
            "title": title,
            "url": link,
            "image_url": img_url,
            "content": "",
            "image_file": None,
        })

    print(f"  Found {len(articles)} articles")

    # visit each article individually to get the full text and cover image
    for i, art in enumerate(articles):
        if not art["url"]:
            continue
        try:
            print(f"  Reading article {i+1}: {art['title'][:55]}...")
            content, page_img = get_article_content(driver, art["url"])
            art["content"] = content
            # if listing page didn't have an image, use the one from article page
            if not art["image_url"] and page_img:
                art["image_url"] = page_img
        except Exception as e:
            print(f"  Could not read article {i+1}: {e}")
            art["content"] = "(could not extract content)"

    # download all the cover images
    for i, art in enumerate(articles):
        if art["image_url"]:
            try:
                art["image_file"] = save_image(art["image_url"], i)
            except Exception as e:
                print(f"  Could not save image {i+1}: {e}")

    return articles
