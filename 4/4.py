import csv

items = list()
with open('text_4_var_66', newline='\n', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    for line in reader:
        item = {
            'id': int(line[0]),
            'name': f"{line[1]} {line[2]}",
            'age': int(line[3]),
            'salary': int(line[4][0:-1])
        }
        items.append(item)

average_salary = sum([item['salary'] for item in items]) / len(items)
filtered = list(filter(lambda item: item['salary'] > average_salary and item['age'] > 25 + 6, items))
sorted = sorted(filtered, key=lambda item: item['id'])

with open('result_4_var_66.csv', encoding='utf-8', newline='\n', mode='w') as result:
    writer = csv.writer(result, delimiter=',')
    for item in sorted:
        writer.writerow(item.values())
