DROP TABLE IF EXISTS libertavoyages_src;


CREATE TABLE IF NOT EXISTS libertavoyages_src (id SERIAL PRIMARY KEY,
                                                                 destination VARCHAR(255),
                                                                             name VARCHAR(255),
                                                                                  stars VARCHAR(1),
                                                                                        check_in DATE, nb_nights INTEGER, nb_adults INTEGER, nb_enfants INTEGER, room_type VARCHAR(255),
                                                                                                                                                                           pension VARCHAR(255),
                                                                                                                                                                                   availability_flag BOOLEAN, availability VARCHAR(255),
                                                                                                                                                                                                                           annulation_flag BOOLEAN, annulation VARCHAR(255),
                                                                                                                                                                                                                                                               price_value DECIMAL, currency VARCHAR(10),
                                                                                                                                                                                                                                                                                             extracted_at TIMESTAMP);


DROP TABLE IF EXISTS traveltodo_src;


CREATE TABLE IF NOT EXISTS traveltodo_src (id SERIAL PRIMARY KEY,
                                                             destination VARCHAR(255),
                                                                         name VARCHAR(255),
                                                                              stars VARCHAR(1),
                                                                                    check_in DATE, nb_nights INTEGER, nb_adults INTEGER, nb_enfants INTEGER, room_type VARCHAR(255),
                                                                                                                                                                       pension VARCHAR(255),
                                                                                                                                                                               availability_flag BOOLEAN, availability VARCHAR(255),
                                                                                                                                                                                                                       annulation_flag BOOLEAN, annulation VARCHAR(255),
                                                                                                                                                                                                                                                           price_value DECIMAL, currency VARCHAR(10),
                                                                                                                                                                                                                                                                                         extracted_at TIMESTAMP);


DROP TABLE IF EXISTS tunisiebooking_src;


CREATE TABLE IF NOT EXISTS tunisiebooking_src (id SERIAL PRIMARY KEY,
                                                                 destination VARCHAR(255),
                                                                             name VARCHAR(255),
                                                                                  stars VARCHAR(1),
                                                                                        check_in DATE, nb_nights INTEGER, nb_adults INTEGER, nb_enfants INTEGER, room_type VARCHAR(255),
                                                                                                                                                                           pension VARCHAR(255),
                                                                                                                                                                                   availability_flag BOOLEAN, availability VARCHAR(255),
                                                                                                                                                                                                                           annulation_flag BOOLEAN, annulation VARCHAR(255),
                                                                                                                                                                                                                                                               price_value DECIMAL, currency VARCHAR(10),
                                                                                                                                                                                                                                                                                             extracted_at TIMESTAMP);


SELECT *
from tunisiebooking_src;


SELECT *
from traveltodo_src;


SELECT *
from traveltodo_src
WHERE availability_flag = FALSE
    and room_type is NULL;


DELETE
FROM traveltodo_src
WHERE room_type IS NULL;


SELECT *
from tunisiebooking_src
WHERE availability_flag = FALSE
    and room_type is NULL;


SELECT *
from libertavoyages_src
WHERE availability_flag = FALSE;

