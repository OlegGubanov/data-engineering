import json
from bs4 import BeautifulSoup
import os
import pandas as pd


def parse_xml(xml):
    soup = BeautifulSoup(xml, 'xml')
    items = soup.find_all('clothing')
    xml_result = []
    for item in items:
        item_result = {}
        for element in item.contents:
            element_value = element.get_text().strip()
            if element.name is None:
                continue
            elif element.name == 'price' or element.name == 'reviews':
                item_result[element.name] = int(element_value)
            elif element.name == 'rating':
                item_result[element.name] = float(element_value)
            elif element.name == 'exclusive' or element.name == 'sporty':
                item_result[element.name] = element_value == "yes"
            elif element.name == 'new':
                item_result[element.name] = element_value == '+'
            else:
                item_result[element.name] = element_value
        xml_result.append(item_result)
    return xml_result


os.chdir('data')
data = []
for filename in os.listdir():
    with open(filename, mode='r', encoding='utf-8') as file:
        data += parse_xml(file)

os.chdir('..')
data = sorted(data, key=lambda item: item['reviews'], reverse=True)
with open('result.json', mode='w', encoding='utf-8') as result:
    result.write(json.dumps(data, indent=4, ensure_ascii=False))

filtered_data = list(filter(lambda item: item['rating'] > 3, data))
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

categories = df['category'].value_counts()
print(categories)