from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Scrapers.dictionary import month_names_en_fr


def select_date(date_container, date):
    try:
        month_year = month_names_en_fr.get(date.strftime("%B")) + " " + str(date.year)
        day = str(date.day)

        date_pickers = date_container.find_elements(By.CLASS_NAME, "drp-calendar")
        while date_pickers[0].find_element(By.CLASS_NAME, "month").text != month_year:
            date_pickers[1].find_element(By.CLASS_NAME, "next").click()
        if date_pickers[0].find_element(By.CLASS_NAME, "month").text == month_year:
            dates = date_pickers[0].find_elements(By.XPATH, "//td")
            for date_el in dates:
                if date_el.text == day:
                    date_el.click()
                    break
    except NoSuchElementException:
        print("Error selecting date!")


def select_nb_adults(driver, nb_adults):
    try:
        container = driver.find_element(By.CLASS_NAME, "groupe_adultes")
        inc_btn = container.find_element(By.ID, 'adplus1')
        dec_btn = container.find_element(By.ID, 'admoins1')
        curr_nb_adults = int(container.find_element(By.CLASS_NAME, 'input_ad').text.strip())
        if curr_nb_adults > nb_adults:
            while curr_nb_adults != nb_adults:
                dec_btn.click()
        elif curr_nb_adults < nb_adults:
            while curr_nb_adults != nb_adults:
                inc_btn.click()
    except NoSuchElementException:
        pass


def select_nb_adults(driver, nb_enfants):
    try:
        container = driver.find_element(By.CLASS_NAME, "groupe_enfants")
        inc_btn = container.find_element(By.ID, 'enplus1')
        dec_btn = container.find_element(By.ID, 'enmoins1')
        curr_nb_enfants = int(container.find_element(By.CLASS_NAME, 'input_ad').text.strip())
        if curr_nb_enfants > nb_enfants:
            while curr_nb_enfants != nb_enfants:
                dec_btn.click()
        elif curr_nb_enfants < nb_enfants:
            while curr_nb_enfants != nb_enfants:
                inc_btn.click()
    except NoSuchElementException:
        pass

def search(driver, destination, arr_date, dep_date, nb_adults, nb_enfants):
    try:
        # Find the hotel search form
        form = driver.find_element(By.ID, "hotel")

        # Find the destination input field within the form and click it
        destination_input = form.find_element(By.ID, "search")
        destination_input.click()

        # Wait for the destination list to appear
        dest_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "liste_dest")))

        # simulate destination list not appearing
        # dest_list = wait.until(EC.presence_of_element_located((By.ID, "liste_destX")))

        # Find all destination list items
        dest_elements = dest_list.find_elements(By.XPATH, "//li[@id='list_dest']")

        # Click on the destination element matching the provided destination
        for element in dest_elements:
            if element.text == destination:
                element.click()
                break

        date_containers = driver.find_elements(By.CLASS_NAME, "daterangepicker")
        select_date(date_containers[0], arr_date)
        select_date(date_containers[1], dep_date)

        select_nb_adults(driver, nb_adults)
        select_nb_adults(driver, nb_enfants)

        # Click the "close" button on the form
        close_button_el = form.find_element(By.CLASS_NAME, "fermer_ch1")
        close_button_el.click()

        # Click the search button
        driver.execute_script("recherche_y();")

        return True
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print("Search Failed!")
        return False
