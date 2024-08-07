import logging
import os
from dotenv import load_dotenv

from Scrapers.AgodaScraper.search import search
from Scrapers.AgodaScraper.extract_hotels_list import get_hotels_list
from Scrapers.utils import init_firefox_driver

load_dotenv()
URL = os.getenv('AGODA_URL')


def scrap(destination, check_in, check_out):
    driver = init_firefox_driver(headless=True)

    print(
        f"Scraping Agoda for hotels in '{destination}' ({check_in.strftime('%Y-%m-%d')} --> {check_out.strftime('%Y-%m-%d')})")
    logging.info(
        f"Scraping Agoda for hotels in '{destination}' ({check_in.strftime('%Y-%m-%d')} --> {check_out.strftime('%Y-%m-%d')})")

    driver.get(URL)

    print("Searching...")
    search(driver, destination, check_in, check_out)

    hotels_links_list = get_hotels_list(driver)
    # print("Scrapping...")
    # results = extract_all_hotels_info(driver)
    # logging.info(f"Processed records: {len(results)}")

    driver.close()

    # return results
