import pickle
import json


def update_price(product, price_change):
    method = price_change['method']
    param = price_change['param']
    if method == 'add':
        product['price'] += param
    elif method == 'sub':
        product['price'] -= param
    elif method == 'percent+':
        product['price'] *= (1 + param)
    elif method == 'percent-':
        product['price'] *= (1 - param)
    product['price'] = round(product['price'], 2)


with open("products_66.pkl", "rb") as file:
    products = pickle.load(file)

with open("price_info_66.json", "r") as file:
    price_changes = json.load(file)

for price_change in price_changes:
    product_name = price_change['name']
    product = list(filter(lambda product: product['name'] == product_name, products)).pop()
    update_price(product, price_change)

with open("updated_products_66.pkl", "wb") as result:
    result.write(pickle.dumps(products))
