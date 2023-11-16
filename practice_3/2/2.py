import re
import json
from bs4 import BeautifulSoup
import os
import pandas as pd


def parse_html(html):
    page_result = []
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('div', {"class": "product-item"})
    for product in products:
        item = {}
        item['id'] = product.find_next('a')['data-id']
        item['image'] = product.find_next('img')['src']
        item['name'] = product.find_next('span').get_text().strip()
        item['price'] = product.find_next('price').get_text().replace('₽', '').replace(' ', '').strip()
        item['bonus'] = product.find_next('strong').get_text().replace('+ начислим ', '').replace(' бонусов', '').strip()
        features = product.find_next('ul')
        for feature in features.find_all('li'):
            item[feature['type']] = feature.get_text().strip()
        page_result.append(item)
    return page_result


os.chdir('data')
data = []
for filename in os.listdir():
    with open(filename, mode='r', encoding='utf-8') as file:
        data += parse_html(file)

os.chdir('..')
data = sorted(data, key=lambda product: int(product['price']), reverse=True)
with open('result.json', mode='w', encoding='utf-8') as result:
    result.write(json.dumps(data, indent=4, ensure_ascii=False))

filtered_data = list(filter(lambda product: int(product['bonus']) > 2500, data))
with open('filtered-result.json', mode='w', encoding='utf-8') as result:
    result.write(json.dumps(filtered_data, indent=4, ensure_ascii=False))

df = pd.read_json('result.json')
price = df['price']
price_sum = f"Сумма: {price.sum()}"
price_max = f"Максимальное значение: {price.max()}"
price_min = f"Минимальное значение: {price.min()}"
price_avr = f"Среднее значение: {price.mean()}"
price_std = f"Стандартное отклоненеие: {price.std()}"
print('price\n' + '\n'.join([price_sum, price_max, price_min, price_avr, price_std]) + '\n')

matrix = df['matrix'].value_counts()
print(matrix)
