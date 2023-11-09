import pandas as pd
import numpy as np
import json
import msgpack
import os

data = pd.read_csv("smoking_dataset.csv", usecols=['sex', 'age', 'height', 'weight', 'waistline',
                                                   'sight_left', 'sight_right', 'hear_left', 'hear_right', 'DRK_YN'])

int_columns = data.select_dtypes(include='int64').columns
data[int_columns] = data[int_columns].astype('float64')

result = []
for column in data.columns:
    column_result = {'column': column}
    if column == 'sex' or column == 'DRK_YN':
        column_result.update(data[column].value_counts(normalize=True).to_dict())
    else:
        column_max = data[column].max()
        column_min = data[column].min()
        column_sum = data[column].sum()
        column_average = column_sum / len(data)
        column_deviation = np.std(data[column])
        column_result.update({"max": column_max, "min": column_min, "sum": column_sum, "avr": column_average,
                              "deviation": column_deviation})
    result.append(column_result)

with open('result_5.json', 'w') as json_result:
    json.dump(result, json_result, indent=4)

data.to_json('smoking_dataset.json', orient='records')
data.to_pickle('smoking_dataset.pkl')

with open('smoking_dataset.msgpack', 'wb') as dataset_msgpack:
    dataset_msgpack.write(msgpack.dumps(data.to_dict()))

files = {'csv': os.path.getsize('smoking_dataset.csv'), 'json': os.path.getsize('smoking_dataset.json'),
         'msgpack': os.path.getsize('smoking_dataset.msgpack'), 'pickle': os.path.getsize('smoking_dataset.pkl')}
print(dict(sorted(files.items(), key=lambda item: item[1])))
