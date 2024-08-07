import logging
import os
from dotenv import load_dotenv

from Scrapers.AgodaScraper.search import search
from Scrapers.utils import init_firefox_driver

load_dotenv()
URL = os.getenv('AGODA_URL')


def scrap(destination, check_in, check_out):
    driver = init_firefox_driver(headless=False)

    print(
        f"Scraping Agoda for hotels in '{destination}' ({check_in.strftime('%Y-%m-%d')} --> {check_out.strftime('%Y-%m-%d')})")
    logging.info(
        f"Scraping Agoda for hotels in '{destination}' ({check_in.strftime('%Y-%m-%d')} --> {check_out.strftime('%Y-%m-%d')})")

    driver.get(URL)

    print("Searching...")
    search(driver, destination, check_in, check_out)

    # print("Scrapping...")
    # results = extract_all_hotels_info(driver)
    # logging.info(f"Processed records: {len(results)}")

    driver.close()

    # return results
