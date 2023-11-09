import requests
from bs4 import BeautifulSoup

requestUrl = 'https://www.cheapshark.com/api/1.0/deals?storeID=1'
data = requests.get(requestUrl).json()

soup = BeautifulSoup("""
<style>
    tr {
    text-align: center;    
}
</style>
<table>
    <tr>
        <th>Game</th>
        <th>Normal Price</th>
        <th>Sale Price</th>
        <th>Savings</th>
        <th>Deal Rating</th>
    </tr>
</table>
""", 'html.parser')

table = soup.find('table')
for item in data:
    tr = soup.new_tag('tr')
    values = item['title'], item['normalPrice'], item['salePrice'], f"{round(float(item['savings']))}%", item['dealRating']
    for value in values:
        td = soup.new_tag('td')
        td.string = value
        tr.append(td)
    table.append(tr)

with open('result_6_var_66.html', encoding='utf-8', mode='w') as result:
    result.write(str(soup.prettify()))
