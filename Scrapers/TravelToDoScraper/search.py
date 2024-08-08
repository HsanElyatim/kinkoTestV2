from selenium.common import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Scrapers.dictionary import month_names_en_fr


def select_destination(driver, search_form, destination):
    """
        Selects the destination in the search form on the webpage.

        Parameters:
            driver (WebDriver): The WebDriver instance.
            search_form (WebElement): The search form WebElement.
            destination (str): The destination city or location to select.

        Returns:
            None
    """
    try:
        # Locate the destination input container
        destination_input_container = search_form.find_element(By.CLASS_NAME, "destination")

        # Find the destination input field within the container
        destination_input = destination_input_container.find_element(By.ID, "locality")

        # Send keys to the destination input field
        destination_input.send_keys(destination)

        # Wait for the destination list container to appear
        destination_list_container = destination_input_container.find_element(By.CLASS_NAME, "tt-dataset-destination")

        # Find all destination list items
        destination_list = destination_list_container.find_elements(By.CLASS_NAME, "tt-suggestion")

        # Click on the first suggestion in the destination list
        driver.execute_script("arguments[0].click();", destination_list[0])

        return True

    except (NoSuchElementException, ElementNotInteractableException, IndexError):
        print("Error selecting destination!")
        return False


def select_date(driver, date_picker, date):
    """
        Selects a specific date from a date picker on a web page.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            date_picker (WebElement): The WebElement representing the date picker.
            date (datetime.date): The date to be selected.

        Returns:
            None
    """
    try:
        # Get the month and day from the provided date
        month = month_names_en_fr.get(date.strftime("%B"))
        day = str(date.day)

        # Scroll the date picker into view
        driver.execute_script("arguments[0].scrollIntoView(true);", date_picker)

        # Find the calendar container
        calendar_containers = date_picker.find_elements(By.CLASS_NAME, "pika-lendar")
        title = calendar_containers[0].find_element(By.CLASS_NAME, "pika-title")

        # Select the month
        month_select = title.find_element(By.CLASS_NAME, "pika-select-month")
        month_select.click()
        months_to_select = month_select.find_elements(By.TAG_NAME, "option")
        for month_to_select in months_to_select:
            if month_to_select.text == month:
                # raise ElementNotInteractableException
                month_to_select.click()
                break

        # Find and click the day element
        calendar_containers = date_picker.find_elements(By.CLASS_NAME, "pika-lendar")
        calendar_body = calendar_containers[0].find_element(By.TAG_NAME, "tbody")
        days_elements = calendar_body.find_elements(By.TAG_NAME, "td")
        for day_el in days_elements:
            if day_el.get_attribute("data-day") == day:
                day_el.click()
                break
    except (NoSuchElementException, ElementNotInteractableException):
        print("Error selecting date!")


def search(driver, destination, arr_date, dep_date):
    """
        Performs a hotel search on a booking website.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            destination (str): The destination to search for.
            arr_date (datetime.date): The arrival date.
            dep_date (datetime.date): The departure date.

        Returns:
            bool: True if the search was successful, False otherwise.
    """
    try:
        # Find the search form
        search_form = driver.find_element(By.ID, "searchForm")

        # Select destination
        if not select_destination(driver, search_form, destination):
            select_destination(driver, search_form, destination)

        # Select arrival and departure dates
        date_pickers = driver.find_elements(By.CLASS_NAME, "pika-single")
        select_date(driver, date_pickers[0], arr_date)
        select_date(driver, date_pickers[1], dep_date)

        # Click on the search button
        search_btn = search_form.find_element(By.CLASS_NAME, "fas")
        search_btn.click()
        return True
    except (NoSuchElementException, ElementNotInteractableException) as e:
        print("Search Failed!")
        return False
