from datetime import datetime

from selenium.common import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Scrapers.dictionary import month_names_en_fr


def select_destination(driver, search_form, destination):
    """
        Selects a destination from an autocomplete dropdown in a search form.

        Parameters:
            driver: selenium.webdriver instance controlling the browser.
            search_form: WebElement representing the search form.
            destination: str, the destination to be selected from the autocomplete suggestions.

        Returns:
            None
    """
    try:
        # Locate the destination input field and enter the destination
        destination_input = search_form.find_element(By.CSS_SELECTOR, "input[data-selenium='textInput']")
        destination_input.send_keys(destination)

        # Wait for the autocomplete panel to be visible
        autocomplete_panel = WebDriverWait(search_form, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div[data-selenium='autocompletePanel']")
        ))

        # Find all autocomplete items and click the one matching the destination
        autosuggest_items = autocomplete_panel.find_elements(By.CSS_SELECTOR,
                                                             "li[data-selenium='autosuggest-item']")
        for autosuggest_item in autosuggest_items:
            if autosuggest_item.get_attribute("data-text") == destination:
                driver.execute_script("arguments[0].click();", autosuggest_item)
                break
    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        print("ERROR selecting destination!")


def select_month(driver, range_picker, month):
    """
        Selects a specific month in a date range picker.

        Parameters:
            driver: selenium.webdriver instance controlling the browser.
            range_picker: WebElement representing the date range picker.
            month: str, the target month in the format "Month Year" (e.g., "June 2024").

        Returns:
            WebElement representing the left calendar of the selected month.
    """
    try:
        # Locate the left calendar within the date range picker
        left_calendar = range_picker.find_element(By.CLASS_NAME, "DayPicker-Month")

        # Loop until the current month matches the target month
        while left_calendar.find_element(By.CLASS_NAME, "DayPicker-Caption").text != month.lower():
            target_month_number = datetime.strptime(month, "%B %Y").month
            current_month_number = datetime.strptime(
                left_calendar.find_element(By.CLASS_NAME, "DayPicker-Caption").text, "%B %Y").month
            if current_month_number < target_month_number:
                driver.execute_script("arguments[0].click();",
                                      range_picker.find_element(By.CSS_SELECTOR, "button[aria-label='Next Month']"))
            else:
                driver.execute_script("arguments[0].click();",
                                      range_picker.find_element(By.CSS_SELECTOR, "button[aria-label='Previous Month']"))
            # Update the left calendar element
            left_calendar = range_picker.find_element(By.CLASS_NAME, "DayPicker-Month")

        # Return the left calendar element of the selected month
        return left_calendar
    except (NoSuchElementException, ElementClickInterceptedException):
        print("ERROR selecting month!")


def select_date(driver, range_picker, day, month):
    """
        Selects a specific date in a date range picker.

        Parameters:
            driver: selenium.webdriver instance controlling the browser.
            range_picker: WebElement representing the date range picker.
            day: str, the day to be selected (e.g., "15").
            month: str, the target month in the format "Month Year" (e.g., "June 2024").

        Returns:
            None
    """
    try:
        # Select the specific month first
        calendar = select_month(driver, range_picker, month)

        # Locate all days within the calendar
        days_picker = calendar.find_elements(By.CLASS_NAME, "PriceSurgePicker-Day")

        # Iterate through days and select the matching day
        for day_picker in days_picker:
            if day_picker.text == day:
                driver.execute_script("arguments[0].click();", day_picker)
                break
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        # print(e)
        print("ERROR selecting date!")


def select_checkin_checkout(driver, search_form, check_in, check_out):
    """
        Selects check-in and check-out dates in a date range picker.

        Parameters:
            driver: selenium.webdriver instance controlling the browser.
            search_form: WebElement representing the search form containing the date range picker.
            check_in: datetime object representing the check-in date.
            check_out: datetime object representing the check-out date.

        Returns:
            None
    """
    check_in_month, check_in_day = month_names_en_fr.get(check_in.strftime("%B")) + " " + str(check_in.year), str(check_in.day)
    check_out_month, check_out_day = month_names_en_fr.get(check_out.strftime("%B")) + " " + str(check_out.year), str(check_out.day)

    try:
        # Locate the range picker within the search form
        range_picker = WebDriverWait(search_form, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div[data-selenium='rangePickerCheckIn']")
        ))

        # Select the check-in date
        select_date(driver, range_picker, check_in_day, check_in_month)

        # Select the check-out date
        select_date(driver, range_picker, check_out_day, check_out_month)
    except TimeoutException:
        print("ERROR selecting check-in check-out!")


def search(driver, destination, check_in, check_out):
    """
        Performs a search operation by selecting destination, check-in, and check-out dates.

        Parameters:
            driver: selenium.webdriver instance controlling the browser.
            destination: str, the destination to search for.
            check_in: datetime object representing the check-in date.
            check_out: datetime object representing the check-out date.

        Returns:
            bool: True if the search was successful, False otherwise.
    """
    try:
        # Locate the search form
        search_form = driver.find_element(By.CSS_SELECTOR, "div[data-selenium='searchBox']")

        # Select the destination
        select_destination(driver, search_form, destination)

        # Select check-in and check-out dates
        select_checkin_checkout(driver, search_form, check_in, check_out)

        # Click the search button
        driver.execute_script(
            "arguments[0].click();",
            driver.find_element(By.CSS_SELECTOR, "button[data-selenium='searchButton']")
        )

        return True
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        # print(e)
        print("Search failed!")
        return False
