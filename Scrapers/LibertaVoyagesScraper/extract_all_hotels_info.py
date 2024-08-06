import logging

from Scrapers.LibertaVoyagesScraper.extract_hotel_info import get_hotel_info
from Scrapers.LibertaVoyagesScraper.extract_hotels_list import extract_hotels_list


def extract_all_hotels_info(driver):
    hotels_infos = []
    hotels_list = extract_hotels_list(driver)

    for hotel in hotels_list:
        hotels_infos.append(get_hotel_info(hotel))

    print(f">> Got info of {len(hotels_infos)}/{len(hotels_list)} hotels.")
    logging.info(f"Got info of {len(hotels_infos)}/{len(hotels_list)} hotels")

    return hotels_infos
