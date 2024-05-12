from time import sleep

import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import allure


XPATH_ACCEPT_COOKIE = "//div[contains(@class, 'Default_container-wrapper')]//button[.//span[contains(@class, 'Button-module_label') and contains(text(), 'Accept')]]"
XPATH_BOT_SIDE = "//div[contains(@class, 'bot-listing_header')]"
XPATH_USER_SIDE = "//div[contains(@class, 'user-listing_header')]"

XPATH_SORT_BUTTON = "//button[contains(@class, 'csm_ui__toggle_button') and @aria-haspopup='listbox' and @aria-expanded='false']"
DEFAULT_PRICE = "//ul[contains(@class, 'csm_ui__options_list')]/li[span[contains(text(), 'Default')]]"
MAX_PRICE = "//ul[contains(@class, 'csm_ui__options_list')]/li[span[contains(text(), 'Price: Max')]]"
MIN_PRICE = "//ul[contains(@class, 'csm_ui__options_list')]/li[span[contains(text(), 'Price: Min')]]"
FLOAT_MAX_PRICE = "//ul[contains(@class, 'csm_ui__options_list')]/li[span[contains(text(), 'Float: Max')]]"
FLOAT_MIN_PRICE = "//ul[contains(@class, 'csm_ui__options_list')]/li[span[contains(text(), 'Float: Min')]]"

# Improved setup_browser function with Allure steps
def setup_browser():
    with allure.step("Настройка браузера"):
        options = Options()
        options.headless = True  # Запуск браузера в фоновом режиме
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

@allure.feature("Тестирование сортировок инвентаря бота")
class TestInventorySorting:

    @allure.story("Сортировка по имени")
    @pytest.fixture(scope="function")
    def setup(self):
        self.driver = setup_browser()
        self.driver.get("https://cs.money/csgo/trade/")
        yield
        if hasattr(self, 'driver'):
            self.driver.quit()

    @allure.testcase("Проверка сортировки по возрастанию имени")
    def test_sort_by_name_ascending(self, setup):
        with allure.step("Принятие куки"):
            try:
                accept_cookie_button = self.driver.find_element(By.XPATH, XPATH_ACCEPT_COOKIE)
                accept_cookie_button.click()
            except NoSuchElementException:
                allure.attach(self.driver.get_screenshot_as_png(), name="Screenshot on Error", attachment_type=allure.attachment_type.PNG)
                raise

        with allure.step("Выбор сортировки по максимальной цене"):
            sort_button = self.driver.find_element(By.XPATH, XPATH_BOT_SIDE + XPATH_SORT_BUTTON)
            sort_button.click()
            sort_by_max_price_button = self.driver.find_element(By.XPATH, XPATH_BOT_SIDE + MAX_PRICE)
            sort_by_max_price_button.click()