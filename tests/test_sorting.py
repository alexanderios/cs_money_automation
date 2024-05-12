import logging

import pytest
from selenium import webdriver

from pages.trade import BotTradePage
from validation import TradeValidation

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@pytest.fixture(scope="class")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.usefixtures("driver")
class TestSorting:
    def test_sort_by_min_price(self, driver):
        """
        Сортировка по цене - от меньшего к большему
        """
        page = BotTradePage(driver)
        page.select_sort_by_min_price()
        inventory_items = page.get_inventory_items()

        validation = TradeValidation()
        validation.check_price_order_ascending(inventory_items)

    def test_sort_by_max_price(self, driver):
        """
        Сортировка по цене - от большего к меньшему
        """
        page = BotTradePage(driver)
        page.select_sort_by_max_price()
        inventory_items = page.get_inventory_items()

        validation = TradeValidation()
        validation.check_price_order_descending(inventory_items)

    def test_sort_by_min_float(self, driver):
        """
        Сортировка по Float инвентора - от меньшего к большему
        """
        page = BotTradePage(driver)
        page.select_sort_by_min_float()
        inventory_items = page.get_inventory_items()

        validation = TradeValidation()
        validation.check_float_order_ascending(inventory_items)

    def test_sort_by_max_float(self, driver):
        """
        Сортировка по Float инвентора - от больше к меньшему
        """
        page = BotTradePage(driver)
        page.select_sort_by_max_float()

        inventory_items = page.get_inventory_items()

        validation = TradeValidation()
        validation.check_float_order_descending(inventory_items)

    def test_sort_min_price_with_same_price(self, driver):
        """
        Проверка сортировки цены в одинаковом ценовом диапазоне по фильтру Min Price
        """
        page = BotTradePage(driver)
        page.set_price_filtering(1, 1)
        inventory_items_before = page.get_inventory_items()

        page.select_sort_by_min_price()

        inventory_items_after = page.get_inventory_items()

        validation = TradeValidation()
        validation.check_stability_on_equal_price(inventory_items_before, inventory_items_after)

    def test_sort_max_price_with_same_price(self, driver):
        """
        Проверка сортировки цены в одинаковом ценовом диапазоне по фильтру Max Price
        """
        page = BotTradePage(driver)
        page.set_price_filtering(1, 1)
        inventory_items_before = page.get_inventory_items()

        page.select_sort_by_max_price()

        inventory_items_after = page.get_inventory_items()

        validation = TradeValidation()
        validation.check_stability_on_equal_price(inventory_items_before, inventory_items_after)

    def test_sort_max_price_with_granite_values(self, driver):
        """
        Проверка сортировки цены в ограниченном ценовом диапазоне
        """
        page = BotTradePage(driver)
        page.set_price_filtering(0.05, 5)

        page.select_sort_by_max_price()
        inventory_items_max = page.get_inventory_items()

        validation = TradeValidation()
        validation.check_item_price(inventory_items_max[0], 5)

        page.select_sort_by_min_price()
        inventory_items_min = page.get_inventory_items()

        validation.check_item_price(inventory_items_min[0], 0.05)
