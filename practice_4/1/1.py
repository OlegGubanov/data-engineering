import pickle
import sqlite3
import json


def get_data(filename):
    with open('task_1_var_66_item.pkl', mode='br') as file:
        return pickle.load(file)


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

    cursor.executemany("""insert into books(title, author, genre, pages, published_year, isbn, rating, views)
        values(:title, :author, :genre, :pages, :published_year, :isbn, :rating, :views)""", data)
    db.commit()

    cursor.close()


def write_data(filename, data):
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def task1(db, filename, limit=76):
    query = 'select * from books order by pages desc limit ?'
    params = [limit]
    ordered_data = execute_query(db, query, params)
    result = [dict(row) for row in ordered_data]

    write_data(filename, result)


def task2(db, filename):
    query = 'select sum(views) as sum, min(views) as min, max(views) as max, avg(views) as avg from books'
    stats = execute_query(db, query).pop()
    result = dict(stats)

    write_data(filename, result)


def task3(db, filename):
    query = """select genre, cast(count() as real) / (select count() from books) as count 
        from books group by genre order by count desc"""
    groups = execute_query(db, query)
    result = [dict(row) for row in groups]

    write_data(filename, result)


def task4(db, filename, rating, limit=76):
    query = 'select * from books where rating > ? order by published_year desc limit ?'
    params = [rating, limit]
    filtered_data = execute_query(db, query, params)
    result = [dict(row) for row in filtered_data]

    write_data(filename, result)


data = get_data('task_1_var_66_item.pkl')
connection = connect_to_db('1_db')
# insert_data(connection, data)

task1(connection, 'ordered_by_pages.json')
task2(connection, 'views_stats.json')
task3(connection, 'grouped_by_genre.json')
task4(connection, 'filtered_by_rating.json', 3)
