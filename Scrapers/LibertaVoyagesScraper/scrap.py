import logging
import os
from dotenv import load_dotenv

from Scrapers.LibertaVoyagesScraper.extract_all_hotels_info import extract_all_hotels_info
from Scrapers.LibertaVoyagesScraper.search import search
from Scrapers.utils import init_firefox_driver

load_dotenv()
URL = os.getenv('LIBERTAVOYAGES_URL')


def scrap(destination, check_in, check_out, nb_adults, nb_enfants):
    driver = init_firefox_driver(headless=True)

    print(
        f"Scraping Liberta for hotels in '{destination}' ({check_in.strftime('%Y-%m-%d')} --> {check_out.strftime('%Y-%m-%d')})")
    logging.info(
        f"Scraping Liberta for hotels in '{destination}' ({check_in.strftime('%Y-%m-%d')} --> {check_out.strftime('%Y-%m-%d')})")

    driver.get(URL)

    print("Searching...")
    search(driver, destination, check_in, check_out, nb_adults, nb_enfants)

    print("Scrapping...")
    results = extract_all_hotels_info(driver)
    logging.info(f"Processed records: {len(results)}")

    driver.close()

    return results
