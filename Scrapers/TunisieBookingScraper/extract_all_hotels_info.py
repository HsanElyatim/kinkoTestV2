from time import sleep
import logging

from Scrapers.TunisieBookingScraper.extract_hotel_info import get_hotel_info
from Scrapers.TunisieBookingScraper.extract_hotels_list import extract_hotels_list


def extract_all_hotels_info(driver):
    """
        Extracts information for all hotels listed on a page.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.

        Returns:
            list: A list of dictionaries containing information about each hotel.
    """
    sleep(10)

    hotels_list = extract_hotels_list(driver)

    hotels_infos = []

    for hotel_id in hotels_list:
        data = get_hotel_info(driver, hotel_id)
        if data is None:
            continue
        hotels_infos.append(data)

    print(f"Got info of {len(hotels_infos)}/{len(hotels_list)} hotels.")
    logging.info(f"Got info of {len(hotels_infos)}/{len(hotels_list)} hotels")

    return hotels_infos
