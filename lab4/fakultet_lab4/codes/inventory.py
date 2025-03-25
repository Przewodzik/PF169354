class Inventory:
    def __init__(self, stockItems=[], isActive=True):
        self.items = stockItems
        self.active = isActive
        self.categories = {}
        self.total_value = 0

    def addItem(self, item, quantity=1):
        for i in range(quantity):
            self.items.append(item)
        if item.category in self.categories:
            self.categories[item.category] += quantity
        else:
            self.categories[item.category] = quantity
        self.calculate_value()

    def calculate_value(self):
        self.total_value = 0
        for item in self.items:
            self.total_value += item.price
        return self.total_value

    def remove_item(self, item, quantity=1):
        removed = 0
        for i in range(len(self.items)):
            if self.items[i] == item and removed < quantity:
                self.items.pop(i)
                removed += 1
                if item.category in self.categories:
                    self.categories[item.category] -= 1
        self.calculate_value()
        return removed


class Product:
    def __init__(self, name, price, category="general"):
        self.name = name
        self.price = price
        self.category = category
        self.__barcode = None

    def set_barcode(self, barcode):
        self.__barcode = barcode

    def get_barcode(self):
        return self.__barcode


class Shop:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.inventory = Inventory()
        self.daily_sales = 0

    def add_product_to_inventory(self, product, quantity=1):
        self.inventory.addItem(product, quantity)

    def sell(self, product, quantity=1):
        removed = self.inventory.remove_item(product, quantity)
        if removed > 0:
            self.daily_sales += product.price * removed
            print(
                f"Sold {removed} {product.name} for a total of ${product.price * removed}"
            )
            return True
        else:
            return False
