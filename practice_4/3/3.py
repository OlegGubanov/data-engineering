import msgpack
import csv
import sqlite3
import json


def read_data_csv(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        data = []
        for i, line in enumerate(reader):
            if i == 0 or not line:
                continue
            else:
                data.append(line)
    return data


def read_data_msgpack(filename):
    with open(filename, mode='br') as file:
        return msgpack.load(file)


def connect_to_db(filename):
    connection = sqlite3.connect(filename)
    # connection.set_trace_callback(print)
    connection.row_factory = sqlite3.Row
    return connection


def execute_query(db, query, params=[]):
    cursor = db.cursor()

    cursor.execute(query, params)
    data = cursor.fetchall()

    cursor.close()
    return data


def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""insert into songs(artist, song, duration_ms, year, tempo, genre) 
        values(:artist, :song, :duration_ms, :year, :tempo, :genre)""", data)
    db.commit()

    cursor.close()


def write_data(filename, data):
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def task1(db, filename, limit=76):
    query = 'select * from songs order by duration_ms desc limit ?'
    params = [limit]
    ordered_data = execute_query(db, query, params)
    result = [dict(row) for row in ordered_data]

    write_data(filename, result)


def task2(db, filename):
    query = 'select sum(tempo) as sum, min(tempo) as min, max(tempo) as max, avg(tempo) as avg from songs'
    stats = execute_query(db, query)
    result = [dict(row) for row in stats]

    write_data(filename, result)


def task3(db, filename):
    query = """select genre, cast(count() as real) / (select count() from songs) as count 
        from songs group by genre order by count desc"""
    groups = execute_query(db, query)
    result = [dict(row) for row in groups]

    write_data(filename, result)


def task4(db, filename, year, limit=81):
    query = 'select * from songs where year > ? order by duration_ms desc limit ?'
    params = [year, limit]
    filtered_data = execute_query(db, query, params)
    result = [dict(row) for row in filtered_data]

    write_data(filename, result)


data_part_1 = read_data_msgpack('task_3_var_66_part_1.msgpack')
data_part_2 = read_data_csv('task_3_var_66_part_2.csv')
connection = connect_to_db('3_db')
# insert_data(connection, data_part_1)
# insert_data(connection, [row[:-3] for row in data_part_2])
task1(connection, 'ordered_by_duration.json')
task2(connection, 'tempo_stats.json')
task3(connection, 'grouped_by_genre.json')
task4(connection, 'filtered_by_year.json', 2015)
