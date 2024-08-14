import logging

from Scrapers.TravelToDoScraper.extract_hotel_info import extract_hotel_info
from Scrapers.TravelToDoScraper.extract_hotels_list import extract_hotels_list


def extract_all_hotels_info(driver):
    """
    Extracts information for all hotels listed on a page.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        list: A list of dictionaries containing information about each hotel.
    """
    hotels_infos = []

    hotels_list = extract_hotels_list(driver)
    if len(hotels_list) == 0:
        print("Return hotels list is empty, retrying...")
        driver.refresh()
        hotels_list = extract_hotels_list(driver)

    for hotel in hotels_list:
        data = extract_hotel_info(driver, hotel)
        if len(data) > 0:
            hotels_infos.append(data)

    print(f">> Got info of {len(hotels_infos)}/{len(hotels_list)} hotels.")
    logging.info(f"Got info of {len(hotels_infos)}/{len(hotels_list)} hotels")

    return hotels_infos
