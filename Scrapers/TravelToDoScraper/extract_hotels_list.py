from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


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

        total_results_count = driver.find_element(By.TAG_NAME, 'h2').text.split(" ")[0]

        # Scroll to the footer
        footer = driver.find_element(By.TAG_NAME, "footer")
        driver.execute_script("arguments[0].scrollIntoView(true);", footer)

        # Wait for a while to ensure all elements are loaded
        sleep(2)

        # Find the results container and extract hotel cards
        results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "results")))
        hotels_list = results.find_elements(By.CLASS_NAME, "card")

        while len(hotels_list) < int(total_results_count):
            hotels_list = results.find_elements(By.CLASS_NAME, "card")

        print(f">> {len(hotels_list)}/{total_results_count} hotel found.")
        return hotels_list
    except (NoSuchElementException, TimeoutException) as e:
        print("Error getting hotels list!")
        return []
