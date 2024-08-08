from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By

from Scrapers.dictionary import month_names_en_fr, month_mapping


def select_destination(search_form, destination):
    try:
        destination_input = search_form.find_element(By.CLASS_NAME, "form-group").find_element(By.TAG_NAME, "input")
        destination_input.send_keys(destination)
        search_form.find_element(By.CLASS_NAME, "form-group").find_element(By.XPATH, "ul/li").click()

        return True
    except (NoSuchElementException, WebDriverException):
        print(f"Destination {destination} not found!")
        return False


def transform_month(month):
    month_abbr, year = month.split(' ')
    full_month = month_mapping.get(month_abbr)
    return f"{full_month} {year}"


def select_date(driver, month, day):
    try:
        calendar_container = driver.find_element(By.CLASS_NAME, "daterangepicker")
        calendar = calendar_container.find_element(By.CLASS_NAME, "left")
        limit = 5
        while transform_month(calendar.find_element(By.CLASS_NAME, "month").text) != month and limit > 0:
            limit -= 1
            driver.find_element(By.CLASS_NAME, "daterangepicker").find_element(By.CLASS_NAME, "right").find_element(
                By.CLASS_NAME, "next").click()
            calendar = driver.find_element(By.CLASS_NAME, "daterangepicker").find_element(By.CLASS_NAME, "left")

        calendar_body = calendar.find_element(By.TAG_NAME, "tbody")
        days_elements = calendar_body.find_elements(By.TAG_NAME, "td")
        for day_el in days_elements:
            if day_el.text == day:
                day_el.click()
                break

        return True
    except NoSuchElementException:
        print("Error handling date selection!")
        return False


def select_checkin_checkout(driver, check_in, check_out, search_form):
    check_in_month, check_in_day = month_names_en_fr.get(check_in.strftime("%B")) + " " + str(check_in.year), str(
        check_in.day)
    check_out_month, check_out_day = month_names_en_fr.get(check_out.strftime("%B")) + " " + str(check_out.year), str(
        check_out.day)

    try:
        search_form.find_element(By.CSS_SELECTOR, "input[name='dates']").click()
        select_date(driver, check_in_month, check_in_day)
        select_date(driver, check_out_month, check_out_day)

        driver.find_element(By.CLASS_NAME, "daterangepicker").find_element(By.CLASS_NAME, "drp-buttons").find_element(
            By.CLASS_NAME, "applyBtn").click()

        return True
    except NoSuchElementException:
        print("Selecting checkin checkout failed!")
        return False


def select_nb_adults(driver, search_form, nb_adults):
    try:
        driver.execute_script("arguments[0].click();", search_form.find_element(By.ID, 'btnNewGroup'))

        nb_adults_selector = search_form.find_element(By.CLASS_NAME, "nbr-adults")
        driver.execute_script("arguments[0].click();", nb_adults_selector)

        options = nb_adults_selector.find_elements(By.TAG_NAME, "option")
        for option in options:
            if option.get_attribute("value") == nb_adults:
                driver.execute_script("arguments[0].click();", option)
                break

        return True
    except NoSuchElementException:
        return False
    

def select_nb_enfants(driver, search_form, nb_enfants):
    try:
        nb_enfants_selector = search_form.find_element(By.CLASS_NAME, "enfants")
        driver.execute_script("arguments[0].click();", nb_enfants_selector)

        options = nb_enfants_selector.find_elements(By.TAG_NAME, "option")
        for option in options:
            if option.get_attribute("value") == nb_enfants:
                driver.execute_script("arguments[0].click();", option)
                break
        
        return True
    except NoSuchElementException:
        return False


def search(driver, destination, check_in, check_out, nb_adults, nb_enfants):
    try:
        search_form = driver.find_element(By.ID, "search_bar")

        select_destination(search_form, destination)

        select_checkin_checkout(driver, check_in, check_out, search_form)

        select_nb_adults(driver, search_form, nb_adults)
        select_nb_enfants(driver, search_form, nb_enfants)
        driver.execute_script("arguments[0].click();", search_form.find_element(By.ID, "btn-check"))

        # driver.execute_script("arguments[0].click();", search_form.find_element(By.CLASS_NAME, "frorm-group").find_element(By.TAG_NAME, "button"))
        search_form.find_element(By.CLASS_NAME, "frorm-group").find_element(By.TAG_NAME, "button").click()

        return True
    except NoSuchElementException:
        print("Search failed!")
        return False
