from pymongo import MongoClient
import pickle
import json
from bson.json_util import dumps


def load_data(filename):
    with open(filename, mode='br') as file:
        data = pickle.load(file)
        return data


def connect_to_database():
    client = MongoClient()
    db = client["my-database"]
    return db.person


def insert_data(db, data):
    db.insert_many(data)


def write_data(filename, data):
    with open(filename, mode='w', encoding='utf-8') as file:
        file.write(data)


def sort_by_salary(db, filename):
    cursor = db.find(limit=10).sort({'salary': -1})
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def filter_by_age(db, filename):
    cursor = db.find({"age": {"$lt": 30}}, limit=15).sort({'salary': -1})
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def predicate_by_city_and_job(db, filename):
    cursor = db.find({"city": "Барселона", "job": {"$in": ["Учитель", "Врач", "Медсестра"]}}, limit=10).sort({'age': 1})
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def filter_by_age_year_salary(db, filename):
    cursor = db.count_documents({
        "age": {"$gt": 27, "$lt": 54},
        "year": {"$in": [2019, 2020, 2021, 2022]},
        "$or": [
            {"salary": {"$gt": 50000, "$lt": 75000}},
            {"salary": {"$gt": 125000, "$lt": 150000}}
        ]
    })
    data = {"count": cursor}
    write_data(filename, json.dumps(data, indent=4))


data = load_data('task_1_item.pkl')
database = connect_to_database()
# insert_data(database, data)
sort_by_salary(database, 'sorted_by_salary.json')
filter_by_age(database, 'filtered_by_age.json')
predicate_by_city_and_job(database, 'teachers_doctors_nurses_from_barсelona.json')
filter_by_age_year_salary(database, 'filtered_by_age_year_salary.json')
