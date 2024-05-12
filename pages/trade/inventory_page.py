from selenium.webdriver.common.by import By
from commons.base_page import BasePage
import allure


class InventoryPage(BasePage):
    ACCEPT_COOKIE = "//div[contains(@class, 'Default_container-wrapper')]//button[.//span[contains(@class, 'Button-module_label') and contains(text(), 'Accept')]]"
    SORT_BUTTON = "//button[substring(@class, 1, 3) = 'csm' and contains(@class, 'ui') and contains(@class, 'toggle') and contains(@class, 'button') and @aria-haspopup='listbox' and @aria-expanded='false']"

    DEFAULT_PRICE = "//ul[contains(@class, 'csm_ui__options_list')]/li[span[contains(text(), 'Default')]]"
    MIN_PRICE = "//ul[contains(@class, 'csm_ui__options_list')]/li[span[contains(text(), 'Price: Min')]]"
    MAX_PRICE = "//ul[contains(@class, 'csm_ui__options_list')]/li[span[contains(text(), 'Price: Max')]]"
    FLOAT_MAX = "//ul[contains(@class, 'csm_ui__options_list')]/li[span[contains(text(), 'Float: Max')]]"
    FLOAT_MIN = "//ul[contains(@class, 'csm_ui__options_list')]/li[span[contains(text(), 'Float: Min')]]"

    def __init__(self, driver, base_xpath):
        super().__init__(driver)
        self.base_xpath = base_xpath
        #self.driver.get("https://cs.money/csgo/trade/")

    def accept_cookies(self):
        with allure.step("Принятие куки"):
            self.click((By.XPATH, self.ACCEPT_COOKIE))

    def select_sort_by_min_price(self):
        with allure.step("Выбор сортировки: Price: Min"):
            self.click((By.XPATH, self.base_xpath + self.SORT_BUTTON))
            self.click((By.XPATH, self.base_xpath + self.MIN_PRICE))

    def select_sort_by_max_price(self):
        with allure.step("Выбор сортировки: Price: Max"):
            self.click((By.XPATH, self.base_xpath + self.SORT_BUTTON))
            self.click((By.XPATH, self.base_xpath + self.MAX_PRICE))

    def select_sort_by_min_float(self):
        with allure.step("Выбор сортировки: Float: Min"):
            self.click((By.XPATH, self.base_xpath + self.SORT_BUTTON))
            self.click((By.XPATH, self.base_xpath + self.FLOAT_MIN))

    def select_sort_by_max_float(self):
        with allure.step("Выбор сортировки: Float: Max"):
            self.click((By.XPATH, self.base_xpath + self.SORT_BUTTON))
            self.click((By.XPATH, self.base_xpath + self.FLOAT_MAX))


class UserTradePage(InventoryPage):
    def __init__(self, driver):
        super().__init__(driver, "//div[contains(@class, 'user-listing_header')]")


class BotTradePage(InventoryPage):
    def __init__(self, driver):
        super().__init__(driver, "//div[contains(@class, 'bot-listing_header')]")
