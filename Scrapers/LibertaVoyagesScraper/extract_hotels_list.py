from time import sleep

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_hotels_list(driver):
    try:
        WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.CLASS_NAME, "loading")))

        sleep(10)
        results_count = driver.find_element(By.ID, "count_hotels").find_element(By.TAG_NAME, "b").text
        hotels_list = driver.find_element(By.ID, "load_hotels_wrapper").find_elements(By.CLASS_NAME, "hotel_div")
        while hotels_list != results_count:
            hotels_list = driver.find_element(By.ID, "load_hotels_wrapper").find_elements(By.CLASS_NAME, "hotel_div")
        
        print(f">> {len(hotels_list)}/{results_count} hotel found.")

        return hotels_list
    except (TimeoutException, NoSuchElementException):
        print("No hotels found")
        return []
