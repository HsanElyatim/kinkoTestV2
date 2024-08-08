from selenium.common import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.by import By

from Scrapers.utils import contains_any


def extract_rooms_info(hotel):
    """
        Extracts room information from a hotel WebElement.

        Args:
            hotel (WebElement): The WebElement representing the hotel.

        Returns:
            list: A list of dictionaries containing room information.
    """
    try:
        # Click the info button to expand room details
        info_btn = hotel.find_element(By.CLASS_NAME, "link-search")
        info_btn.click()

        # Find the container for room information
        container = hotel.find_element(By.CLASS_NAME, "lstrooms")
        rooms = container.find_elements(By.CLASS_NAME, "item-room")

        rooms_info = []
        for room in rooms:
            # Extract room name
            name_x = room.find_element(By.CLASS_NAME, "mb-2").text.strip().split(" ")
            name = []
            for i in name_x[2::]:
                if contains_any(i, ["disponible", "complet", "sur", "non", "minimum"]):
                    break
                name.append(i)
            name = " ".join(name)

            # Check room availability
            availability_message = (room.find_element(By.CLASS_NAME, "badge").text.strip())
            availability = True if availability_message == "Disponible" else False

            # Check if cancellation is free
            annulation_message = room.find_element(By.CLASS_NAME, "rateDescription").text.strip()
            annulation = True if "gratuite" in annulation_message else False

            # Iterate over pension options
            pension_select = room.find_element(By.TAG_NAME, "select")
            pension_list = pension_select.find_elements(By.TAG_NAME, "option")
            for pension in pension_list:
                pension.click()
                price_value = float(room.find_element(By.CLASS_NAME, "price").get_attribute("value"))

                rooms_info.append({
                    "name": name,
                    "pension": pension.text,
                    "price_value": price_value,
                    "currency": "TND",
                    "availability_flag": availability,
                    "availability": availability_message,
                    "annulation_flag": annulation,
                    "annulation": annulation_message
                })

        return rooms_info
    except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
        # print("Error getting rooms info!")
        return []


def extract_hotel_info(driver, hotel):
    """
        Extracts information about a hotel including its name, star rating, and room details.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            hotel (WebElement): The WebElement representing the hotel.

        Returns:
            list: A list of dictionaries containing hotel information.
    """
    try:
        # Scroll to the hotel element
        driver.execute_script("arguments[0].scrollIntoView();", hotel)

        # Extract hotel name
        name = hotel.find_element(By.CLASS_NAME, "h3").text.strip()

        # Extract hotel star rating
        stars = str(len(hotel.find_element(By.CLASS_NAME, "h3").find_elements(By.TAG_NAME, "i")))

        # Extract room information
        rooms_info = extract_rooms_info(hotel)
        hotel_info = []
        if len(rooms_info) > 0:
            for room in rooms_info:
                if len(room) == 0 :
                    pass
                hotel_info.append({
                    "name": name,
                    "stars": stars,
                    "room_type": room["name"],
                    "pension": room["pension"],
                    "availability_flag": room["availability_flag"],
                    "availability": room["availability"],
                    "annulation_flag": room["annulation_flag"],
                    "annulation": room["annulation"],
                    "price_value": room["price_value"],
                    "currency": room["currency"]
                })

        else:
            print(name)
            availability_msgs = hotel.find_elements(By.CLASS_NAME, "displayAvailDates")
            availability = availability_msgs[1].text.strip() if len(availability_msgs) > 1 else None
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
    except NoSuchElementException:
        print("Error getting hotel info!")
        return []
