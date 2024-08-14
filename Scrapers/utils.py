import json
import re
from functools import wraps
import time
from selenium import webdriver

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class CustomError(Exception):
    pass


def init_chrome_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--lang=fr')
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # service = Service(executable_path="/usr/local/bin/chromedriver")
    # driver = webdriver.Chrome(service=service, options=options)

    return driver


def init_firefox_driver(headless=True):
    """
        Initializes a headless Firefox WebDriver with specific options for scraping.

        Returns:
            WebDriver: Initialized Firefox WebDriver instance.
    """
    # Set up Firefox options
    firefox_options = FirefoxOptions()
    if headless: 
        firefox_options.add_argument("--headless")  # Run in headless mode
    firefox_options.add_argument("--no-sandbox")  # Required for running as root user
    firefox_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    firefox_options.set_preference("intl.accept_languages", "fr")

    # Initialize the WebDriver for Firefox
    driver = webdriver.Firefox(options=firefox_options)

    geckodriver_path = "/usr/local/bin/geckodriver"
    # service = FirefoxService(executable_path=geckodriver_path)

    # driver = webdriver.Firefox(service=service, options=firefox_options)

    if not headless:
        driver.maximize_window()

    return driver

def extract_hotel_number(string):
    """Extracts the last integer from a string, handling variations and edge cases.

    Args:
        string: The input string.

    Returns:
        The extracted integer, or None if no valid number is found.
    """

    # Handle common variations:
    if string.endswith("_"):
        string = string[:-1]  # Remove trailing underscore

    # Match a sequence of digits, optionally preceded by a sign:
    match = re.search(r"[-+]?\d+$", string)

    if match:
        # Extract the number and convert to integer:
        return int(match.group())
    else:
        # No valid number found
        return None


def write_extracted_infos(file_path, data):
    """
    Writes the provided data to a JSON file at the specified path.

    Args:
        file_path (str): The path to the output JSON file.
        data (any): The data to be serialized and written to the file.

    Raises:
        Exception: If any errors occur during file opening or JSON serialization.
    """
    try:
        # Open the file in write mode and assign it to json_file
        with open(file_path, "w") as json_file:
            # Serialize the data to JSON format and write it to the file with indentation
            json.dump(data, json_file, indent=4)
    except Exception as e:
        print(f"Error writing data to file: {e}")


def contains_any(text, words):
    """
      Checks if a string 'text' contains any of the words in the list 'words'.

      Args:
          text: The string to search.
          words: A list of words to check for.

      Returns:
          True if the text contains any of the words, False otherwise.
    """
    for word in words:
        if word in text.lower():  # Case-insensitive check
            return True
    return False
