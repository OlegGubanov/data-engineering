import csv

from bs4 import BeautifulSoup

items = list()
with open('text_5_var_66', encoding='utf-8', mode='r') as file:
    soup = BeautifulSoup(file, 'html.parser')
    rows = soup.find_all('tr')[1:]
    for row in rows:
        item = row.find_all('td')
        items.append([i.text for i in item])

with open('result_5_var_66.csv', encoding='utf-8', newline='\n', mode='w') as result:
    writer = csv.writer(result, delimiter=',')
    for item in items:
        writer.writerow(item)
