from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv
import logging

import pandas as pd
from sqlalchemy import create_engine

from Scrapers.TravelToDoScraper.scrap import scrap as traveltodo_scrap
from Scrapers.LibertaVoyagesScraper.scrap import scrap as libertavoyages_scrap
from Scrapers.TunisieBookingScraper.scrap import scrap as tunisiebooking_scrap

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
skip_days_for_test = 4
check_in = datetime.today().date() + timedelta(days=skip_days_for_test)
nb_nights = 1
check_out = datetime.today().date() + timedelta(days=nb_nights) + timedelta(days=skip_days_for_test)


def transform_load(data, table_name):
    flattened_data = [item for sublist in data for item in sublist]
    # pprint.pprint(flattened_data)

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
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f">> {len(df)} records saved!")


def execute_scrap(source, destination, check_in, check_out):
    function_name = f"{source}_scrap"
    if function_name in globals():
        return globals()[function_name](destination, check_in, check_out)
    else:
        raise ValueError(f"Function {function_name} does not exist")


# Start the script execution
logging.info("Script started")

start_time = time.time()

for destination in TARGET_DESTINATIONS:
    for source in SCRAPING_SOURCES:
        max_retry = 3
        results = execute_scrap(source, destination, check_in, check_out)
        if len(results) == 0:
            i = 0
            while i < MAX_RETRY:
                i += 1
                print(f"Retry {i}/{MAX_RETRY}")

                results = execute_scrap(source, destination, check_in, check_out)
                if len(results) > 0:
                    break
        transform_load(results, f"{source}_src")
        print("###########################")

print("-----------------------")
end_time = time.time()
print(f"Done in {end_time - start_time}")
print("-----------------------")

logging.info(f"Script completed")
logging.info(f"Total execution time: {end_time - start_time:.2f} seconds")
