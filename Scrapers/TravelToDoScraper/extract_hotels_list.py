from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
from dotenv import load_dotenv

from selenium.common import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

load_dotenv()
MAX_RETRY = int(os.getenv('MAX_RETRY'))


def extract_hotels_list(driver):
    """
        Retrieves a list of hotels from the search results page.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.

        Returns:
            list: A list of WebElement representing hotels.
    """
    try:
        # Wait until the loading indicator disappears
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "loading-result")))

        try:
            total_results_count = int(driver.find_element(By.TAG_NAME, 'h2').text.split(" ")[0])
        except ValueError:
                print("ERROR")
                return []
        print(total_results_count)

        # Scroll to the footer
        footer = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "footer"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", footer)

        # Wait for a while to ensure all elements are loaded
        sleep(20)

        # Find the results container and extract hotel cards
        results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "results")))
        hotels_list = results.find_elements(By.CLASS_NAME, "card")
        print(len(hotels_list))

        retry = 0
        while len(hotels_list) != total_results_count and retry < MAX_RETRY:
            retry += 1
            print("Error")
            hotels_list = results.find_elements(By.CLASS_NAME, "card")

        print(f">> {len(hotels_list)}/{total_results_count} hotel found.")
        return hotels_list
    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        print("Error getting hotels list!")
        return []
