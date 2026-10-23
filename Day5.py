catalog = {"apple": 40, "milk": 55, "bread": 30}   # name: price
cart = {}                                          # name: quantity

def add_to_cart(item, qty=1):
    if item not in catalog:
        print("Product not found")
        return
    cart[item] = cart.get(item, 0) + qty

def remove_from_cart(item):
    cart.pop(item, None)

def show_cart():
    total = 0
    for item, qty in cart.items():
        cost = catalog[item] * qty
        total += cost
        print(f"{item:10} x{qty}  = {cost}")
    print("Total:", total)

add_to_cart("apple", 3)
add_to_cart("milk")
show_cart()