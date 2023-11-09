import json
import msgpack
import os

products = dict()
with open("products_66.json", 'r') as file:
    data = json.load(file)
    for item in data:
        name = item['name']
        price = item['price']
        if name in products:
            products[name].append(price)
        else:
            products[name] = [price]

result = []
for name, prices in products.items():
    prices_average = sum(prices) / len(prices)
    prices_max = max(prices)
    prices_min = min(prices)
    result.append({'name': name, 'max': prices_max, 'min': prices_min, 'avr': prices_average})

with open("products_result_66.json", 'w') as result_json:
    result_json.write(json.dumps(result))

with open("products_result_66.msgpack", "wb") as result_msgpack:
    result_msgpack.write(msgpack.dumps(result))

print(os.path.getsize("products_result_66.json"))
print(os.path.getsize("products_result_66.msgpack"))
