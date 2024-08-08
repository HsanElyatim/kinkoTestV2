from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Scrapers.utils import extract_hotel_number


def extract_pensions(hotel_el):
    try:
        pensions_el_container = WebDriverWait(hotel_el, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pension")))
        pensions_el = pensions_el_container.find_elements(By.TAG_NAME, "div")
        if len(pensions_el) < 1:
            return None
        pension_dict = {}
        for pension in pensions_el:
            if (pension.get_attribute("id") != ""
                    and pension.text != ""
                    and pension.get_attribute("id") not in pension_dict.keys()):
                pension_dict[pension.get_attribute("id")] = pension.text
        return pension_dict
    except (NoSuchElementException, TimeoutException):
        print("No pensions found!")


def get_rooms_info(hotel_el, h_id):
    try:
        # hotel_el.find_element(By.CLASS_NAME, "lien_call_prix").click()

        pension_dict = extract_pensions(hotel_el)
        if pension_dict is None:
            return []
        room_types = {}
        for room in hotel_el.find_element(By.ID, f"div_pension1_{list(pension_dict.keys())[0]}_{h_id}").find_elements(
                By.TAG_NAME, "label"):
            key = room.find_element(By.TAG_NAME, "input").get_attribute("id")
            value = room.find_element(By.CLASS_NAME, "span_lib_ch").text

            if key not in room_types.keys() and value != "":
                room_types[key] = value
        # print(room_types)
        rooms_info = []
        for pension_short, pension_name in pension_dict.items():
            rooms_container = hotel_el.find_element(By.ID, f"div_pension1_{pension_short}_{h_id}")
            room_elements = rooms_container.find_elements(By.TAG_NAME, "label")

            for room in room_elements:
                key = room.find_element(By.TAG_NAME, "input").get_attribute("id")
                value = room.find_element(By.CLASS_NAME, "span_lib_ch").text.strip()
                if key not in room_types.keys() and value != "":
                    room_types[key] = value

                availability_message = room.find_element(By.XPATH, '..').find_element(By.CLASS_NAME,
                                                                                      "span_stock").text.strip()
                availability = True if "Disponible" in availability_message else False

                price_value = room.find_element(By.TAG_NAME, "input").get_attribute("value")

                rooms_info.append({
                    'name': value if value != "" else "Unknown",
                    "pension": pension_name,
                    "availability_flag": availability,
                    "availability": availability_message,
                    'price_value': price_value,
                    "currency": "TND"
                })

        # print(rooms)
        return rooms_info
    except NoSuchElementException as e:
        print("Error getting rooms info", e)
        return []


def get_hotel_info(driver, hotel_id):
    try:
        hotel_el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, hotel_id)))
        driver.execute_script("arguments[0].scrollIntoView(true);", hotel_el)

        h_id = hotel_el.get_attribute("id")
        h_id = extract_hotel_number(h_id)
        name = hotel_el.find_element(By.ID, "libelle_hotel").text
        try:
            stars = hotel_el.find_element(By.CLASS_NAME, "etoliess").text
        except NoSuchElementException:
            stars = 0

        facerd = hotel_el.find_element(By.ID, f"facerd{h_id}")
        try:
            annulation_message = facerd.find_element(By.CLASS_NAME, "annul_gratuit").text.strip()
            annulation = True if "Gratuite" in annulation_message else False
        except NoSuchElementException:
            annulation = False
            annulation_message = "Not Found"

        rooms_info = get_rooms_info(hotel_el, h_id)

        hotel_info = []
        
        if len(rooms_info) > 0:
            for room in rooms_info:
                hotel_info.append({
                    "name": name,
                    "stars": stars,
                    "room_type": room["name"],
                    "pension": room["pension"],
                    "availability_flag": room["availability_flag"],
                    "availability": room["availability"],
                    "annulation_flag": annulation,
                    "annulation": annulation_message,
                    "price_value": room["price_value"],
                    "currency": room["currency"]
                })
        else:
            availability = hotel_el.find_element(By.CLASS_NAME, 'text_erreur').text.strip()
            hotel_info.append({
                    "name": name,
                    "stars": stars,
                    "room_type": None,
                    "pension": None,
                    "availability_flag": False,
                    "availability": availability,
                    "annulation_flag": None,
                    "annulation": None,
                    "price_value": None,
                    "currency": None
                })

        return hotel_info
    except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
        print("Error getting hotel info!")
        return []
