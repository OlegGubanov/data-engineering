import csv
import json
from pymongo import MongoClient


def load_data():
    persons = []
    reader = csv.DictReader(open('task_3_item.csv', encoding='utf-8'), delimiter=';')
    for row in reader:
        person = {}
        pairs = row.items()
        for pair in pairs:
            key = pair[0]
            value = pair[1]
            if key in ['salary', 'id', 'year', 'age']:
                person[key] = int(value)
            elif key in ['job', 'city']:
                person[key] = value
        persons.append(person)
    return persons


def connect_to_database():
    client = MongoClient()
    db = client["my-database"]
    return db.person


def insert_data(db, data):
    db.insert_many(data)


def delete_by_salary(db):
    result = db.delete_many({
        "$or": [
            {"salary": {"$lt": 25000}},
            {"salary": {"$gt": 175000}}
        ]
    })

    print(result)


def update_age(db):
    result = db.update_many({}, {
        "$inc": {
            "age": 1
        }
    })

    print(result)


def increase_salary_by_job(db):
    filter = {
        "job": {"$in": ['Учитель', 'Врач', 'Медсестра']}
    }
    update = {
        "$mul": {
            "salary": 1.05
        }
    }

    result = db.update_many(filter, update)
    print(result)


def increase_salary_by_city(db):
    filter = {
        "city": {"$in": ['Подгорица', 'Загреб', 'Краков']}
    }
    update = {
        "$mul": {
            "salary": 1.07
        }
    }

    result = db.update_many(filter, update)
    print(result)


def increase_salary_by_complex_predicate(db):
    filter = {
        "city": {"$nin": ['Подгорица', 'Загреб', 'Краков']},
        "job": {"$nin": ['Учитель', 'Врач', 'Медсестра']},
        "age": {"$gte": 18, "$lte": 23}
    }

    update = {
        "$mul": {
            "salary": 1.1
        }
    }

    result = db.update_many(filter, update)
    print(result)


def delete_by_salary_and_age(db):
    filter = {
        "age": {"$lt": 20},
        "salary": {"$gt": 150000}
    }

    result = db.delete_many(filter)
    print(result)



connection = connect_to_database()
data = load_data()
# insert_data(connection, data)
# delete_by_salary(connection)
# update_age(connection)
# increase_salary_by_job(connection)
# increase_salary_by_city(connection)
# increase_salary_by_complex_predicate(connection)
# delete_by_salary_and_age(connection)
