class Price:
    def __init__(self, price_str):
        parts = price_str.strip().split(' ')
        self.currency = parts[0]
        num_part = ''.join(parts[1:]).replace(' ', '').replace(',', '.')
        self.value = float(num_part)


class FloatValue:
    def __init__(self, float_str):
        try:
            if '/' in float_str:
                parts = float_str.split('/')
                self.float_type = ' / '.join(parts[:-1]).strip()
                self.value = float(parts[-1].strip())
            else:
                self.float_type = float_str.strip()
                self.value = None
        except (IndexError, ValueError):
            self.float_type = float_str
            self.value = None


class InventoryItem:
    def __init__(self, card_id=None, price_str=None, float_str=None):
        self.card_id = card_id
        self.price = Price(price_str) if price_str else None
        self.float_value = FloatValue(float_str) if float_str else None