
class ShoppingCart:

    def __init__(self):
        self.items = {}

    def add_item(self,item_name, price , quantity):

        if item_name in self.items:
            self.items[item_name]['quantity'] += quantity

        else:
            self.items[item_name] = {'quantity': quantity, 'price': price}

    def remove_item(self,item_name):
        if item_name in self.items:
            del self.items[item_name]
        else:
            raise ValueError('Item not found')

    def get_total(self):
        return sum(item['quantity'] * item['price'] for item in self.items.values())

    def clear(self):
        self.items.clear()



cart = ShoppingCart()

cart.add_item("Apple", 10, 1)
cart.add_item("Apple", 10, 2)
cart.add_item("Banana", 10, 3)
cart.add_item("Lemon", 10, 4)
print(len(cart.items))

