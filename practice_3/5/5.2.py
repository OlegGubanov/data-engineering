from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import pandas as pd
import json


def get_page(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    with Chrome(options=chrome_options) as browser:
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        return soup


# links = pd.read_json('result.json')['href'].to_list()
# items = []
# i = 0
# while True:
#     if i == 10:
#         break
#     print(i)
#     link = links[i]
#     url = link + 'properties/'
#     soup = get_page(url)
#     item = {}
#     item['name'] = soup.find('h1').get_text().replace('Характеристики ', '')
#     item['price'] = int(soup.find('span', {"data-meta-price": True})['data-meta-price'].replace(' ', ''))
#     characteristics = (soup.find(lambda tag: tag.name == 'span' and 'Характеристики' in tag.text)
#                        .find_next('ul').find_all('li'))
#     for ch_item in characteristics:
#         divs = ch_item.find_all('div', recursive=False)
#         for div in divs:
#             div_text = div.get_text(separator='separator').split('separator')
#             key = div_text[0].strip()
#             value = div_text[1].strip()
#             if value.strip() == 'вспышки':
#                 continue
#             item[key] = value
#     try:
#         print(item['Год релиза'])
#         i = i + 1
#     except:
#         continue
#     items.append(item)
#
# data = sorted(items, key=lambda item: int(item['Год релиза']), reverse=True)
# with open('result-2.json', mode='w', encoding='utf-8') as result2_json:
#     result2_json.write(json.dumps(data, indent=4, ensure_ascii=False))
#
# filtered_data = list(filter(lambda item: item['price'] > 100000, items))
# with open('filtered-result-2.json', mode='w', encoding='utf-8') as filtered_result2_json:
#     filtered_result2_json.write(json.dumps(filtered_data, indent=4, ensure_ascii=False))

df = pd.read_json('result-2.json')
df['Вес товара'] = df['Вес товара'].apply(lambda row: row.split()[0]).astype('float')
weight = df['Вес товара']
weight_sum = f"Сумма: {weight.sum()}"
weight_max = f"Максимальное значение: {weight.max()}"
weight_min = f"Минимальное значение: {weight.min()}"
weight_avr = f"Среднее значение: {weight.mean()}"
weight_std = f"Стандартное отклоненеие: {weight.std()}"
print('Вес товара\n' + '\n'.join([weight_sum, weight_max, weight_min, weight_avr, weight_std]) + '\n')

brands = df['Бренд'].value_counts()
print(brands)
