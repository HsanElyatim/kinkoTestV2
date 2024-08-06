from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def extract_hotels_list(driver):
    try:
        result = driver.find_element(By.ID, "ruslt_dispo")
        hotels_el_list = result.find_elements(By.CLASS_NAME, "hotel_y_prom")
        hotels_ids_list = [hotel_el.get_attribute("id") for hotel_el in hotels_el_list]
        print(f">> {len(hotels_ids_list)} hotel found.")
        return hotels_ids_list
    except NoSuchElementException:
        print("No hotels found!")
        return []
