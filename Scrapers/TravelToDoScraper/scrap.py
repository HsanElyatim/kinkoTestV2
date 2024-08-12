import logging
import os
from dotenv import load_dotenv

from Scrapers.TravelToDoScraper.extract_all_hotels_info import extract_all_hotels_info
from Scrapers.utils import init_firefox_driver
from Scrapers.TravelToDoScraper.search import search

load_dotenv()
URL = os.getenv('TRAVELTODO_URL')


def scrap(destination, check_in, check_out, nb_adults, nb_enfants):
    """
        Scrapes Travel To Do website for hotels information based on the provided destination, check-in, and check-out dates.

        Parameters:
            destination (str): The destination city or location.
            check_in (datetime.date): The check-in date.
            check_out (datetime.date): The check-out date.

        Returns:
            None
    """
    driver = init_firefox_driver(headless=True)

    print(
        f"Scraping Travel To Do for hotels in {destination} ({check_in.strftime('%Y-%m-%d')} --> {check_out.strftime('%Y-%m-%d')})")
    logging.info(
        f"Scraping Travel To Do for hotels in {destination} ({check_in.strftime('%Y-%m-%d')} --> {check_out.strftime('%Y-%m-%d')})")

    driver.get(URL)

    print("Searching...")
    if not search(driver, destination, check_in, check_out, nb_adults, nb_enfants):
        driver.close()
        driver = init_firefox_driver()
        driver.get(URL)

    print("Scrapping...")
    results = extract_all_hotels_info(driver)
    logging.info(f"Processed records: {len(results)}")

    driver.close()

    return results
