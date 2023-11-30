import msgpack
import sqlite3
import json


def load_data(filename):
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

    cursor.executemany("insert into sales(title, price, place, date) values(:title, :price, :place, :date)", data)
    db.commit()

    cursor.close()


def write_data(filename, data):
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# средняя цена, по которой продавались книги, у которых рейтинг больше 4
def first_query(db, filename):
    query = """
    select avg(price) as price from sales 
    where title in (select title from books where rating > 4)"""
    price = execute_query(db, query)
    result = [dict(row) for row in price]
    write_data(filename, result)


# все продажи книг Льва Толстого
def second_query(db, filename):
    query = """
    select * from sales
    where title in (select title from books where author = "Лев Толстой")
    """
    sales = execute_query(db, query)
    result = [dict(row) for row in sales]
    write_data(filename, result)


# количество продаж книг, которые были опубликованы позже 2020 года
def third_query(db, filename):
    query = """
    select count() as count from sales 
    where title in (select title from books where published_year > '2020')
    """
    sales = execute_query(db, query)
    result = [dict(row) for row in sales]
    write_data(filename, result)


data = load_data('task_2_var_66_subitem.msgpack')
connection = connect_to_db('2_db')
# insert_data(connection, data)
first_query(connection, 'average_price_rating_greater_4.json')
second_query(connection, 'sales_tolstoy.json')
third_query(connection, 'prices_count_published_after_2020.json')