import pprint
import time
import psycopg2
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
import psutil

from Scrapers.TunisieBookingScraper.scrap import scrap
from Scrapers.dictionary import DESTINATIONS

start_time = time.time()

process = psutil.Process()

# Database connection parameters
dbname = 'kinkotest'
user = 'postgres'
password = 'hsan'
host = 'localhost'
port = '5432'

# Create the table if it does not exist
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)
create_table_query = '''
CREATE TABLE IF NOT EXISTS tunisiebooking_src (
    id SERIAL PRIMARY KEY,
    destination VARCHAR(255),
    name VARCHAR(255),
    check_in DATE,
    nb_nights INTEGER,
    stars VARCHAR(1),
    room_type VARCHAR(255),
    pension VARCHAR(255),
    availability_flag BOOLEAN,
    availability VARCHAR(255),
    annulation_flag BOOLEAN,
    annulation VARCHAR(255),
    price_value DECIMAL,
    currency VARCHAR(10),
    extracted_at TIMESTAMP
);
'''
cur = conn.cursor()
cur.execute(create_table_query)
conn.commit()
cur.close()
conn.close()

# Scrap data
destination = DESTINATIONS[0]
check_in = datetime.today().date()
nb_nights = 1
check_out = datetime.today().date() + timedelta(days=nb_nights)

# scrap(destination, check_in, check_out)

for destination in DESTINATIONS:
    data = scrap(destination, check_in, check_out)
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
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')

    df.to_sql('tunisiebooking_src', engine, if_exists='append', index=False)
    print(f"# {len(df)} records saved!")

print("-----------------------")
# print_process_resource_usage()

end_time = time.time()

print(f"Done in {end_time - start_time}")
print("-----------------------")
