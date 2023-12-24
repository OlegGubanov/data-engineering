import pandas as pd
import os
import json


def write_data(filename, data):
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def write_memory_stats(filename, df):
    file_size = os.path.getsize('[2]automotive.csv.zip')
    print(f'file size: {file_size // 1024} КБ')
    memory_usage_by_columns = df.memory_usage(deep=True)
    total_memory_usage = memory_usage_by_columns.sum()
    print(f'file size in memory: {total_memory_usage // 1024} КБ')
    column_stats = list()
    for column in df.dtypes.keys():
        column_stats.append({
            "column": column,
            "memory_abs": int(memory_usage_by_columns[column] // 1024),
            "memory_per": float(round(memory_usage_by_columns[column] / total_memory_usage * 100, 4)),
            "dtype": str(df.dtypes[column])
        })

    column_stats.sort(key=lambda x: x['memory_abs'], reverse=True)
    write_data(filename, column_stats)


def optimize_objects(df):
    object_columns = df.select_dtypes(include=['object'])

    for column in object_columns:
        num_unique_values = len(df[column].unique())
        num_total_values = len(df[column])
        if num_unique_values / num_total_values < 0.5:
            df[column] = df[column].astype('category')


def optimize_ints(df):
    int_columns = df.select_dtypes(include=['int']).columns
    df[int_columns] = df[int_columns].apply(pd.to_numeric, downcast='signed')


def optimize_floats(df):
    float_columns = df.select_dtypes(include=['float']).columns
    df[float_columns] = df[float_columns].apply(pd.to_numeric, downcast='float')


def optimize_dataframe(df):
    optimize_objects(df)
    optimize_ints(df)
    optimize_floats(df)

    return df


# df = pd.read_csv('[2]automotive.csv.zip')
# write_memory_stats('memory_stats_without_optimization.json', df)
#
# optimized_df = optimize_dataframe(df.copy())
# write_memory_stats('memory_stats_with_optimization.json', optimized_df)

columns_dtypes = {
    'firstSeen': pd.StringDtype,
    'lastSeen': pd.StringDtype,
    'askPrice': pd.StringDtype,
    'isNew': pd.CategoricalDtype,
    'color': pd.CategoricalDtype,
    'brandName': pd.CategoricalDtype,
    'vf_BasePrice': pd.StringDtype,
    'vf_Seats': pd.StringDtype,
    'vf_TopSpeedMPH': pd.StringDtype,
    'vf_VehicleType': pd.CategoricalDtype
}

# write_header = True
# for chunk in pd.read_csv('[2]automotive.csv.zip',
#                          usecols=lambda column: column in columns_dtypes.keys(),
#                          dtype=columns_dtypes,
#                          chunksize=100000):
#     chunk.dropna().to_csv('df.csv', mode='a', header=write_header, index=False)
#     write_header = False
