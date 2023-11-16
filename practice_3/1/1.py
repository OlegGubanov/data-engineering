import re
import json
from bs4 import BeautifulSoup
import os
import pandas as pd


def parse_html(html):
    building = dict()
    soup = BeautifulSoup(html, 'html.parser')
    building['city'] = soup.find('span').get_text().strip().replace('Город: ', '')
    building['title'] = (soup.find('h1', {"class": "title"}).get_text().replace('\n', '').replace('Строение:', '').strip())
    address = (soup.find('p', {"class": "address-p"}).get_text().replace('\n', '').strip().replace('    ', ''))
    address_split = address.split('Индекс:')
    street = address_split[0].replace('Улица: ', '').strip()
    index = address_split[1].strip()
    building['street'] = street
    building['index'] = index
    building['floors'] = soup.find('span', {"class": "floors"}).get_text().replace('Этажи:', '').strip()
    building['year'] = soup.find('span', {"class": "year"}).get_text().replace('Построено в', '').strip()
    building['parking'] = soup.find('span', string=re.compile('Парковка')).get_text().replace('Парковка:', '').strip()
    building['image'] = soup.find('img')['src']
    building['rating'] = soup.find('span', string=re.compile('Рейтинг')).get_text().replace('Рейтинг:', '').strip()
    building['views'] = soup.find('span', string=re.compile('Просмотры')).get_text().replace('Просмотры:', '').strip()
    return building


os.chdir('data')
data = []
for filename in os.listdir():
    with open(filename, mode='r', encoding='utf-8') as file:
        data.append(parse_html(file))

os.chdir('..')
data = sorted(data, key=lambda building: int(building['year']), reverse=True)
with open('result.json', mode='w', encoding='utf-8') as result:
    result.write(json.dumps(data, indent=4, ensure_ascii=False))

filtered_data = list(filter(lambda building: int(building['views']) > 50000, data))
with open('filtered-result.json', mode='w', encoding='utf-8') as result:
    result.write(json.dumps(filtered_data, indent=4, ensure_ascii=False))

df = pd.read_json('result.json')
views = df['views']
views_sum = f"Сумма: {views.sum()}"
views_max = f"Максимальное значение: {views.max()}"
views_min = f"Минимальное значение: {views.min()}"
views_avr = f"Среднее значение: {views.mean()}"
views_std = f"Стандартное отклоненеие: {views.std()}"
print('views\n' + '\n'.join([views_sum, views_max, views_min, views_avr, views_std]) + '\n')

parking = df['parking'].value_counts()
print(parking)
