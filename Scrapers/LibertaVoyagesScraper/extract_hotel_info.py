from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By


def get_pensions_list(hotel):
    try:
        return [el.text for el in hotel.find_element(By.CLASS_NAME, "liste-pensions").find_elements(By.TAG_NAME, "a")]
    except NoSuchElementException:
        print("Error getting pensions!")
        return []


def get_rooms_list(hotel):
    pensions = get_pensions_list(hotel)
    try:
        rooms_per_pensions = hotel.find_element(By.CLASS_NAME, "tab-content").find_elements(By.CLASS_NAME, "tab-pane")
        rooms_list = []
        for pension in pensions:
            for rooms_per_pension in rooms_per_pensions:
                rooms_list.append((pension, rooms_per_pension))

        return rooms_list
    except NoSuchElementException:
        print("Error getting rooms list!")
        return []


def get_rooms_info(hotel):
    try:
        rooms_per_pensions = get_rooms_list(hotel)

        rooms_info = []
        for el in rooms_per_pensions:
            rooms = el[1].find_elements(By.TAG_NAME, 'option')
            for room in rooms:
                room_name = room.get_attribute("data-libelle")
                price_value = room.get_attribute("data-tarif")
                availability_message = hotel.find_element(By.ID, "btn-disponibilite").text.strip()
                if availability_message.lower() == "disponible":
                    availability_flag = True
                else:
                    availability_flag = False

                rooms_info.append({
                    "name": room_name,
                    "pension": el[0],
                    "price_value": price_value,
                    "currency": "TND",
                    "availability_flag": availability_flag,
                    "availability_message": availability_message
                })

        return rooms_info
    except NoSuchElementException as e:
        print("Error getting rooms info!")
        return []


def get_hotel_info(hotel):
    try:
        hotel_desc = hotel.find_element(By.CLASS_NAME, "desc")
        hotel_name = hotel_desc.find_element(By.TAG_NAME, "h3").text.strip()

        try:
            hotel_stars = len(hotel_desc.find_elements(By.TAG_NAME, "img"))
        except NoSuchElementException:
            hotel_stars = hotel_desc.find_elements(By.TAG_NAME, "strong").text.spli(' ')[0]

        hotel_info = []
        for room in get_rooms_info(hotel):
            hotel_info.append({
                "name": hotel_name,
                "stars": hotel_stars,
                "room_type": room["name"],
                "pension": room["pension"],
                "availability_flag": room["availability_flag"],
                "availability": room["availability_message"],
                "annulation_flag": None,
                "annulation": "UNKNOWN",
                "price_value": room["price_value"],
                "currency": room["currency"]
            })

        return hotel_info
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        print("Failed extracting hotel info!")
        return []
