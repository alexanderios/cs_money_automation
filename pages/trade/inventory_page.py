import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from commons.base_page import BasePage
from pages.trade.inventory_page_models import InventoryItem


class InventoryPage(BasePage):

    ACCEPT_COOKIE = "//div[contains(@class, 'Default_container-wrapper')]//button[.//span[contains(@class, 'Button-module_label') and contains(text(), 'Accept')]]"

    SORT_BUTTON = "//button[substring(@class, 1, 3) = 'csm' and contains(@class, 'ui') and contains(@class, 'toggle') and contains(@class, 'button') and @aria-haspopup='listbox' and @aria-expanded='false']"
    DEFAULT_PRICE = "//*[@id[substring(., string-length(.) - string-length('-item-0') + 1) = '-item-0']]"
    MAX_PRICE = "//*[@id[substring(., string-length(.) - string-length('-item-1') + 1) = '-item-1']]"
    MIN_PRICE = "//*[@id[substring(., string-length(.) - string-length('-item-2') + 1) = '-item-2']]"
    FLOAT_MAX = "//*[@id[substring(., string-length(.) - string-length('-item-3') + 1) = '-item-3']]"
    FLOAT_MIN = "//*[@id[substring(., string-length(.) - string-length('-item-4') + 1) = '-item-4']]"

    PRICE_FROM = "//div[contains(@class, 'FilterPrice_inputs')]//input[contains(@placeholder, '$ 0.00')]"
    PRICE_TO = "//div[contains(@class, 'FilterPrice_inputs')]//input[contains(@placeholder, '$ ∞')]"
    FLOAT_FROM = "//span[text()='Float']/ancestor::div//input[contains(@placeholder, '0.0000')]"
    FLOAT_TO = "//span[text()='Float']/ancestor::div//input[contains(@placeholder, '1')]"
    RESET_BUTTON = "//button[contains(@class, 'button') and .//span[contains(text(), 'Reset')]]"

    def __init__(self, driver, base_xpath):
        super().__init__(driver)
        self.base_xpath = base_xpath
        self.driver.get("https://cs.money/csgo/trade/")
        self.accept_cookies_if_present()

    def accept_cookies_if_present(self):
        try:
            cookie_button = self.driver.find_element(By.XPATH, self.ACCEPT_COOKIE)
            if cookie_button.is_displayed():
                cookie_button.click()
                self.logger.info("Cookie acceptance button clicked.")
        except NoSuchElementException:
            self.logger.info("No cookie acceptance button present.")

    def select_sort_by_min_price(self):
        with allure.step("Выбор сортировки: Price: Min"):
            self.click((By.XPATH, self.base_xpath + self.SORT_BUTTON))
            self.move_and_click((By.XPATH, self.base_xpath + self.MIN_PRICE))

    def select_sort_by_max_price(self):
        with allure.step("Выбор сортировки: Price: Max"):
            self.click((By.XPATH, self.base_xpath + self.SORT_BUTTON))
            self.move_and_click((By.XPATH, self.base_xpath + self.MAX_PRICE))

    def select_sort_by_min_float(self):
        with allure.step("Выбор сортировки: Float: Min"):
            self.click((By.XPATH, self.base_xpath + self.SORT_BUTTON))
            self.move_and_click((By.XPATH, self.base_xpath + self.FLOAT_MIN))

    def select_sort_by_max_float(self):
        with allure.step("Выбор сортировки: Float: Max"):
            self.click((By.XPATH, self.base_xpath + self.SORT_BUTTON))
            self.move_and_click((By.XPATH, self.base_xpath + self.FLOAT_MAX))

    def set_price_filtering(self, price_from, price_to):
        with allure.step(f"Установка фильтрации по цене с ${price_from} до ${price_to}"):
            self.input((By.XPATH, self.PRICE_FROM), price_from)
            self.input((By.XPATH, self.PRICE_TO), price_to)

    def set_float_filtering(self, float_from, float_to):
        with allure.step(f"Установка фильтрации по качеству с ${float_from} до ${float_to}"):
            self.input((By.XPATH, self.FLOAT_FROM), float_from)
            self.input((By.XPATH, self.FLOAT_TO), float_to)

    def click_reset(self):
        with allure.step("Сброс настроек фильтрации"):
            self.click((By.XPATH, self.RESET_BUTTON))

    def get_inventory_items(self):
        with allure.step("Получение первых 6 элементов из списка инвентаря"):
            try:
                items = WebDriverWait(self.driver, 10).until(
                    lambda driver: [element for element in driver.find_elements(By.XPATH, "//div[contains(@class, 'actioncard_card')]") if len(driver.find_elements(By.XPATH, "//div[contains(@class, 'actioncard_card')]")) >= 6][:6]
                )

                if not items:
                    raise RuntimeError("No inventory items found.")

                inventory_items = []

                for item in items:
                    card_info = item.find_element(By.XPATH, ".//div[@data-id='trade_item_bot_add']")
                    card_id = card_info.get_attribute("data-card-id")

                    price_path = f".//div[@data-card-id='{card_id}']//div[contains(@class,'BaseCard_price')]//span[contains(@class, 'styles_price')]"
                    float_path = f".//div[@data-card-id='{card_id}']//div[contains(@class,'BaseCard_description')]//span[contains(@class, 'CSGODescription_description')]"

                    float_element = item.find_element(By.XPATH, float_path).text
                    price = item.find_element(By.XPATH, price_path).text
                    inventory_item = InventoryItem(card_id=card_id, price_str=price, float_str=float_element)
                    inventory_items.append(inventory_item)

                return inventory_items
            except TimeoutException:
                raise TimeoutException("The inventory items did not load within the expected time.")


class UserTradePage(InventoryPage):
    def __init__(self, driver):
        super().__init__(driver, "//div[contains(@class, 'user-listing_header')]")


class BotTradePage(InventoryPage):
    def __init__(self, driver):
        super().__init__(driver, "//div[contains(@class, 'bot-listing_header')]")