# coding=utf-8
"""
.. codeauthor:: Maciej 'maQ' Kusz
"""

from wait_for_angular import WaitForAngular
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import time

WAIT_FOR_ANGULAR_FULL_PAGE_LOAD = 300


class WaitType(object):
    """ Predefined wait types
    """
    STANDARD = 0
    ANGULAR_NO_EXT = 1
    ANGULAR_EXT = 2


def open_page(wait_type):
    """ Open web page with angular with different wait types

    :param wait_type: WaitType
    :return: value of wait time for page load
    """
    # Define WebDriver
    if wait_type == WaitType.ANGULAR_NO_EXT:
        options = ChromeOptions()
        options.add_argument("--disable-extensions")
        web_driver = Chrome(chrome_options=options)
    else:
        web_driver = Chrome()

    web_driver.get('https://www.cherrycasino.com/en/')  # Open web page with angular
    start_time = time()  # Start counting wait time

    # Define wait condition
    if wait_type == WaitType.STANDARD:
        condition = expected_conditions.invisibility_of_element_located((By.XPATH, "//div[@class='loader']"))
    else:
        condition = WaitForAngular()

    # Wait for element based on condition
    WebDriverWait(web_driver, timeout=WAIT_FOR_ANGULAR_FULL_PAGE_LOAD).until(condition)
    time_taken = round((time() - start_time), 2)  # Calculate value of wait time
    web_driver.quit()  # Exit WebDriver
    return time_taken  # Return value of wait time

# Usage example
print("Waiting for page load took {} seconds (no Angular check)".format(open_page(WaitType.STANDARD)))
print("Waiting for Angular took {} seconds (Chrome extensions enabled)".format(open_page(WaitType.ANGULAR_NO_EXT)))
print("Waiting for Angular took {} seconds (Chrome extensions disabled)".format(open_page(WaitType.ANGULAR_EXT)))
