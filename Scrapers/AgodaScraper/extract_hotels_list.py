from time import sleep
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_hotel_link(driver, hotel_elm):
    """
        Retrieves the link to the hotel from a hotel element on the search results page.

        Parameters:
            driver: selenium.webdriver instance controlling the browser.
            hotel_elm: WebElement representing the hotel element.

        Returns:
            str: The URL link to the hotel, or None if an error occurs.
    """
    try:
        # Scroll the hotel element into view
        driver.execute_script("arguments[0].scrollIntoView(true);", hotel_elm)

        # Return the hotel link
        return hotel_elm.find_element(By.TAG_NAME, "a").get_attribute("href")
    except (NoSuchElementException, StaleElementReferenceException) as e:
        print("ERROR getting hotel link!")


def get_hotels_list(driver):
    """
        Retrieves a list of hotel links from the hotel list view on a booking website.

        Parameters:
            driver: WebDriver instance used to interact with the web page.

        Returns:
            list: A list of strings representing URLs to each hotel's details page.
                  Returns an empty list if no hotels are found or if an error occurs.
    """
    try:
        sleep(5)  # Pause to ensure content loads
        hotel_filter = driver.find_element(By.CSS_SELECTOR,
                                           "span[data-component='search-filter-accommodationtype'][aria-label='Hôtel']")
        total_results = hotel_filter.find_element(By.CSS_SELECTOR,"span[data-selenium='filter-count']").text.strip().replace("(", "").replace(")", "")
        driver.execute_script("arguments[0].click();", hotel_filter)

        # Wait for the hotel list container to be visible
        hotels_list_container = WebDriverWait(driver, 10) \
            .until(EC.visibility_of_element_located((By.CLASS_NAME, 'hotel-list-container')))

        # Wait for all hotel items to be present in the list
        hotels_list = WebDriverWait(hotels_list_container, 10) \
            .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[data-selenium='hotel-item']")))

        # Extract links for each hotel item
        hotel_links = [get_hotel_link(driver, hotel_elm) for hotel_elm in hotels_list]

        # Scroll to the last hotel item and footer to load more hotels
        driver.execute_script("arguments[0].scrollIntoView(true);", hotels_list[-1])
        sleep(2)  # Pause for scrolling
        driver.execute_script("arguments[0].scrollIntoView(true);",
                              driver.find_element(By.CLASS_NAME, "Footer"))

        sleep(5)  # Pause to load more content

        # Fetch additional hotels from the second container if available
        hotels_list_containers = driver.find_elements(By.CLASS_NAME, 'hotel-list-container')

        hotels_list2 = WebDriverWait(hotels_list_containers[1], 10) \
            .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[data-selenium='hotel-item']")))
        hotel_links2 = [get_hotel_link(driver, hotel_elm) for hotel_elm in hotels_list2]
        hotel_links.extend(hotel_links2)

        print(f">> {len(hotel_links)}/{total_results} hotel found.")

        return hotel_links
    except (NoSuchElementException, TimeoutException) as e:
        print(e)
        print("ERROR getting hotels list!")
        return []