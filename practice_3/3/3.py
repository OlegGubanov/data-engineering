import json
from bs4 import BeautifulSoup
import os
import pandas as pd


def parse_xml(xml):
    soup = BeautifulSoup(xml, 'xml')
    star = soup.star
    item = {}
    for element in star.contents:
        if element.name is not None:
            item[element.name] = (element.get_text().replace(' days', '')
                                  .replace(' billion years', '').replace('million km', '').strip())
    return item


os.chdir('data')
data = []
for filename in os.listdir():
    with open(filename, mode='r', encoding='utf-8') as file:
        data.append(parse_xml(file))


os.chdir('..')
data = sorted(data, key=lambda star: int(star['radius']), reverse=True)
with open('result.json', mode='w', encoding='utf-8') as result:
    result.write(json.dumps(data, indent=4, ensure_ascii=False))

filtered_data = list(filter(lambda star: float(star['age']) > 3, data))
with open('filtered-result.json', mode='w', encoding='utf-8') as result:
    result.write(json.dumps(filtered_data, indent=4, ensure_ascii=False))

df = pd.read_json('result.json')
distance = df['distance']
distance_sum = f"Сумма: {distance.sum()}"
distance_max = f"Максимальное значение: {distance.max()}"
distance_min = f"Минимальное значение: {distance.min()}"
distance_avr = f"Среднее значение: {distance.mean()}"
distance_std = f"Стандартное отклоненеие: {distance.std()}"
print('distance\n' + '\n'.join([distance_sum, distance_max, distance_min, distance_avr, distance_std]) + '\n')

constellation = df['constellation'].value_counts()
print(constellation)
