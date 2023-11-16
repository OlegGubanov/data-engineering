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


# url = 'https://www.citilink.ru/catalog/smartfony/'
# soup = get_page(url)
# pages = soup.find_all('a', {"data-meta-name": lambda name: name and name.startswith('PageLink__page')})
# last_page = int(pages[-2].get_text())
# result = []
# for page in range(1, last_page + 1):
#     page_result = []
#     items_soup = get_page(f"{url}?p={page}")
#     items = items_soup.find_all('div',
#                                 {"data-meta-name": lambda name: name and name.startswith('ProductHorizontalSnippet')})
#     for item in items:
#         item_result = {}
#         item_result['id'] = (item.find(lambda tag: tag.name == 'span' and 'Код товара:' in tag.text).get_text()
#                              .replace('Код товара: ', ''))
#         item_result['href'] = 'https://www.citilink.ru' + item.find('a', target=False)['href']
#         item_result['img'] = item.find('img', {"class": "is-selected"})['src']
#         item_result['name'] = item.find('a', title=True).get_text()
#         properties = item.find('ul').find_all('li')
#         for prop in properties:
#             prop_name = prop.find('span').get_text().replace(u'\xa0', u'')
#             prop_value = prop.find(string=True, recursive=False)
#             if prop_value[-1] == ',' or prop_value[-1] == ';':
#                 prop_value = prop_value[:-1]
#             item_result[prop_name] = prop_value
#         item_result['price'] = int(item.find('span', {"data-meta-price": True})['data-meta-price'])
#         page_result.append(item_result)
#
#     result += page_result
#     break
#
# data = sorted(result, key=lambda item: item['price'], reverse=True)
# with open('result.json', mode='w', encoding='utf-8') as result_json:
#     result_json.write(json.dumps(data, indent=4, ensure_ascii=False))
#
# filtered_data = list(filter(lambda item: not item['Процессор'].startswith('MediaTek'), result))
# with open('filtered-result.json', mode='w', encoding='utf-8') as filtered_result_json:
#     filtered_result_json.write(json.dumps(filtered_data, indent=4, ensure_ascii=False))

df = pd.read_json('result.json')
price = df['price']
price_sum = f"Сумма: {price.sum()}"
price_max = f"Максимальное значение: {price.max()}"
price_min = f"Минимальное значение: {price.min()}"
price_avr = f"Среднее значение: {price.mean()}"
price_std = f"Стандартное отклоненеие: {price.std()}"
print('price\n' + '\n'.join([price_sum, price_max, price_min, price_avr, price_std]) + '\n')

processors = df['Процессор'].value_counts()
print(processors)
