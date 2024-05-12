import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import safe_action


class BasePage:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)

    @safe_action
    def click(self, by_locator):
        try:
            self.logger.debug(f"Attempting to click on element with locator: {by_locator}")
            element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(by_locator))
            element.click()
            self.logger.info(f"Clicked on element with locator: {by_locator}")
        except TimeoutException:
            self.logger.error(f"TimeoutException: Element with locator {by_locator} not visible within 5 seconds.")

    @safe_action
    def input(self, by_locator, value):
        try:
            self.logger.debug(f"Attempting to input text into element with locator: {by_locator}")
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
            element.send_keys(value)
            self.logger.info(f"Inputted text into element with locator: {by_locator}")
        except TimeoutException:
            self.logger.error(f"TimeoutException: Element with locator {by_locator} not found within the timeout period.")

    @safe_action
    def is_visible(self, by_locator):
        try:
            self.logger.debug(f"Checking visibility of element with locator: {by_locator}")
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
            self.logger.info(f"Element with locator: {by_locator} is visible.")
            return bool(element)
        except TimeoutException:
            self.logger.warning(f"Element with locator: {by_locator} is not visible within timeout period.")
            return False

    @safe_action
    def move_and_click(self, by_locator):
        try:
            self.logger.debug(f"Attempting to move to and click on element with locator: {by_locator}")
            element_to_click = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator))
            actions = ActionChains(self.driver)
            actions.move_to_element(element_to_click).click().perform()
            self.logger.info(f"Moved to and clicked on element with locator: {by_locator}")
        except TimeoutException:
            self.logger.error(
                f"TimeoutException: Element with locator {by_locator} could not be clicked within the timeout period.")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
