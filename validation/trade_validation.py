import allure


class TradeValidation:
    @staticmethod
    def check_price_order_ascending(inventory_items):
        with allure.step("Проверка сортировки цен по возрастанию"):
            prices = [item.price.value for item in inventory_items]
            if prices == sorted(prices):
                allure.attach(f"Цены отсортированы правильно: {prices}", name="Сортировка верна")
            else:
                allure.attach(f"Цены отсортированы некорректно: {prices}", name="Ошибка сортировки")

    @staticmethod
    def check_price_order_descending(inventory_items):
        with allure.step("Проверка сортировки цен по убыванию"):
            prices = [item.price.value for item in inventory_items]
            if prices == sorted(prices, reverse=True):
                allure.attach(f"Цены отсортированы правильно: {prices}", name="Сортировка верна")
            else:
                allure.attach(f"Цены отсортированы некорректно: {prices}", name="Ошибка сортировки")

    @staticmethod
    def check_float_order_ascending(inventory_items):
        with allure.step("Проверка сортировки float по возрастанию"):
            floats = [item.float_value.value for item in inventory_items]
            if floats == sorted(floats):
                allure.attach(f"Float значения отсортированы правильно: {floats}", name="Сортировка верна")
            else:
                allure.attach(f"Float значения отсортированы некорректно: {floats}", name="Ошибка сортировки")

    @staticmethod
    def check_float_order_descending(inventory_items):
        with allure.step("Проверка сортировки float по убыванию"):
            floats = [item.float_value.value for item in inventory_items]
            if floats == sorted(floats, reverse=True):
                allure.attach(f"Float значения отсортированы правильно: {floats}", name="Сортировка верна")
            else:
                allure.attach(f"Float значения отсортированы некорректно: {floats}", name="Ошибка сортировки")

    @staticmethod
    def check_stability_on_equal_price(inventory_items_before, inventory_items_after):
        with allure.step("Проверка стабильности сортировки при одинаковых ценах"):
            if len(inventory_items_before) != len(inventory_items_after):
                allure.attach("Количество предметов в списках различается", name="Ошибка сортировки")
                return

            all_equal = True
            for item_before, item_after in zip(inventory_items_before, inventory_items_after):
                if item_before.card_id != item_after.card_id or item_before.price.value != item_after.price.value:
                    all_equal = False
                    break

            if all_equal:
                allure.attach("Порядок и цены карточек остались неизменными", name="Сортировка стабильна")
            else:
                allure.attach("Порядок или цены карточек изменились", name="Ошибка сортировки")

    @staticmethod
    def check_item_price(item, expected_price):
        with allure.step(f"Проверка цены элемента {item.card_id} на соответствие ожидаемой цене"):
            actual_price = item.price.value
            if actual_price == expected_price:
                allure.attach(
                    f"Цена элемента соответствует ожидаемой: ожидаемая {expected_price}, фактическая {actual_price}",
                    name="Цена верна")
            else:
                allure.attach(
                    f"Цена элемента не соответствует ожидаемой: ожидаемая {expected_price}, фактическая {actual_price}",
                    name="Ошибка цены")