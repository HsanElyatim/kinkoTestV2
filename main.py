from datetime import datetime, timedelta
import time
import os
import argparse
from dotenv import load_dotenv
import logging

import pandas as pd
from sqlalchemy import create_engine

from Scrapers.utils import init_firefox_driver
from Scrapers.TravelToDoScraper.scrap import scrap as traveltodo_scrap
from Scrapers.LibertaVoyagesScraper.scrap import scrap as libertavoyages_scrap
from Scrapers.TunisieBookingScraper.scrap import scrap as tunisiebooking_scrap
# from Scrapers.AgodaScraper.scrap import scrap as agoda_scrap

# Configure logging
logging.basicConfig(filename='script_report.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

DB_NAME = os.getenv('POSTGRES_DB_NAME')
DB_USER = os.getenv('POSTGRES_DB_USER')
DB_PASSWORD = os.getenv('POSTGRES_DB_PASSWORD')
DB_HOST = os.getenv('POSTGRES_DB_HOST')
DB_PORT = os.getenv('POSTGRES_DB_PORT')
MAX_RETRY = int(os.getenv('MAX_RETRY'))
SCRAPING_SOURCES = os.getenv('SCRAPING_SOURCES').split(',')
TARGET_DESTINATIONS = os.getenv('TARGET_DESTINATIONS').split(',')

# Script Params
# skip_days_for_test = 0
# check_in = datetime.today().date() + timedelta(days=skip_days_for_test)
# nb_nights = 1
# check_out = datetime.today().date() + timedelta(days=nb_nights) + timedelta(days=skip_days_for_test)


def transform_load(data, table_name, engine):
    flattened_data = [item for sublist in data for item in sublist]

    df = pd.DataFrame(flattened_data)

    df["nb_nights"] = nb_nights
    df['destination'] = destination
    df['check_in'] = check_in
    df['extracted_at'] = datetime.now()

    # Convert appropriate columns to datetime types
    df['check_in'] = pd.to_datetime(df['check_in'])
    df['extracted_at'] = pd.to_datetime(df['extracted_at'])

    # Save data
    print("Saving to DB...")

    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f">> {len(df)} records saved!")


# def execute_scrap(source, destination, check_in, check_out):
#     function_name = f"{source}_scrap"
#     if function_name in globals():
#         return globals()[function_name](destination, check_in, check_out)
#     else:
#         raise ValueError(f"Function {function_name} does not exist")

def get_scrap_function(source_name):
    return {
        "traveltodo": traveltodo_scrap,
        "tunisiebooking": tunisiebooking_scrap,
        "libertavoyages": libertavoyages_scrap
    }.get(source_name)


# for destination in TARGET_DESTINATIONS:
#     for source in SCRAPING_SOURCES:
#         max_retry = 3
#         results = execute_scrap(source, destination, check_in, check_out)
#         if len(results) == 0:
#             i = 0
#             while i < MAX_RETRY:
#                 i += 1
#                 print(f"Retry {i}/{MAX_RETRY}")

#                 results = execute_scrap(source, destination, check_in, check_out)
#                 if len(results) > 0:
#                     break
#         transform_load(results, f"{source}_src")
#         print("###########################")


def main():
    logging.info("Script started")

    start_time = time.time()
    
    # Initialize database connection
    POSTGRES_DB_CONN = {
        'DB_NAME': os.getenv('POSTGRES_DB_NAME'),
        'USER': os.getenv('POSTGRES_DB_USER'),
        'PWD': os.getenv('POSTGRES_DB_PASSWORD'),
        'HOST': os.getenv('POSTGRES_DB_HOST'),
        'PORT': os.getenv('POSTGRES_DB_PORT')
    }
    db_url = f"postgresql://{POSTGRES_DB_CONN['USER']}:{POSTGRES_DB_CONN['PWD']}@{POSTGRES_DB_CONN['HOST']}:{POSTGRES_DB_CONN['PORT']}/{POSTGRES_DB_CONN['DB_NAME']}"
    engine = create_engine(db_url)

    SCRAPING_SOURCES = os.getenv('SCRAPING_SOURCES').split(',')
    TARGET_DESTINATIONS = os.getenv('TARGET_DESTINATIONS').split(',')

    sources = args.sources.split(',') if isinstance(args.sources, str) else args.sources
    destinations = args.destinations.split(',') if isinstance(args.destinations, str) else args.destinations
    check_in = datetime.datetime.strptime(args.check_in, "%Y-%m-%d").date()
    check_out = datetime.datetime.strptime(args.check_out, "%Y-%m-%d").date()

    driver = init_firefox_driver

    for source_name in sources:
        if source_name not in SCRAPING_SOURCES:
            print(f"Unknown scraping source: {source_name}")
            continue

        scrap_function = get_scrap_function(source_name)
        if scrap_function is None:
            print(f"Unknown scraping source: {source_name}")
            continue

        for destination in destinations:
            if destination not in TARGET_DESTINATIONS:
                print(f"Unknown destination: {destination}")
                continue

            # Scrape data
            data = scrap_function(driver, destination, check_in, check_out)

            # Transform and load data into the database
            transform_load(data, f"{source_name}_src", engine)


    print("-----------------------")
    end_time = time.time()
    print(f"Done in {end_time - start_time}")
    print("-----------------------")

    logging.info(f"Script completed")
    logging.info(f"Total execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape travel data and store in a database.')
    parser.add_argument('--sources', type=str, required=True, help='The source(s) for scraping, comma-separated (e.g., traveltodo,tunisiebooking,libertavoyages)')
    parser.add_argument('--destinations', type=str, required=True, help='The destination(s) for scraping, comma-separated (e.g., Hammamet,Tunis)')
    parser.add_argument('--check_in', type=str, required=True, help='Check-in date in YYYY-MM-DD format')
    parser.add_argument('--check_out', type=str, required=True, help='Check-out date in YYYY-MM-DD format')

    args = parser.parse_args()
    main(args)