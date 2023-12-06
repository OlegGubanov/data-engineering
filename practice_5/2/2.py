import json
from pymongo import MongoClient
from bson.json_util import dumps


def load_data():
    with open('task_2_item.json', mode='r', encoding='utf-8') as file:
        data = json.load(file)
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


def stats_by_salary(db, filename):
    query = [
        {
            "$group": {
                "_id": None,
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"},
                "max": {"$max": "$salary"}
            }
        }
    ]

    cursor = db.aggregate(query)
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def count_by_job(db, filename):
    query = [
        {
            "$group": {
                "_id": "$job",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]

    cursor = db.aggregate(query)
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def property_stats_by_column(db, property, column, filename):
    query = [
        {
            "$group": {
                "_id": f"${column}",
                "min": {"$min": f"${property}"},
                "avg": {"$avg": f"${property}"},
                "max": {"$max": f"${property}"}
            }
        },
        {
            "$sort": {
                "_id": 1
            }
        }
    ]

    cursor = db.aggregate(query)
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def max_salary_with_min_age(db, filename):
    query = [
        {
            "$match": {
                "age": 18
            }
        },
        {
            "$group": {
                "_id": None,
                "age": {"$min": "$age"},
                "salary": {"$max": "$salary"}
            }
        }
    ]

    cursor = db.aggregate(query)
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def min_salary_with_max_age(db, filename):
    query = [
        {
            "$match": {
                "age": 65
            }
        },
        {
            "$group": {
                "_id": None,
                "age": {"$max": "$age"},
                "salary": {"$min": "$salary"}
            }
        }
    ]

    cursor = db.aggregate(query)
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def age_stats_with_filter_by_salary(db, filename):
    query = [
        {
            "$match": {
                "salary": {"$gt": 50000}
            }
        },
        {
            "$group": {
                "_id": "$city",
                "min": {"$min": "$age"},
                "avg": {"$avg": "$age"},
                "max": {"$max": "$age"}
            }
        },
        {
            "$sort": {
                "_id": 1
            }
        }
    ]

    cursor = db.aggregate(query)
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def salary_stats_filter_by_city_job_age(db, filename):
    query = [
        {
            "$match": {
                "city": {"$in": ["Валенсия", "Севилья", "Эльче"]},
                "job": {"$in": ["Архитектор", "Строитель"]},
                "$or": [
                    {"age": {"$gt": 18, "$lt": 25}},
                    {"age": {"$gt": 50, "$lt": 65}}
                ]
            }
        },
        {
            "$group": {
                "_id": None,
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"},
                "max": {"$max": "$salary"}
            }
        }
    ]

    cursor = db.aggregate(query)
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def salary_stats_filter_by_city(db, filename):
    query = [
        {
            "$match": {
                "city": {"$in": ['Москва', 'Астана', 'Минск']}
            }
        },
        {
            "$group": {
                "_id": "$city",
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"},
                "max": {"$max": "$salary"}
            }
        },
        {
            "$sort": {
                "avg": -1
            }
        }
    ]

    cursor = db.aggregate(query)
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


data = load_data()
database = connect_to_database()
# insert_data(database, data)
stats_by_salary(database, 'stats_by_salary.json')
count_by_job(database, 'count_by_job.json')
property_stats_by_column(database, 'salary', 'city', 'salary_stats_by_city.json')
property_stats_by_column(database, 'salary', 'job', 'salary_stats_by_job.json')
property_stats_by_column(database, 'age', 'city', 'age_stats_by_job.json')
property_stats_by_column(database, 'age', 'job', 'age_stats_by_job.json')
max_salary_with_min_age(database, 'max_salary_with_min_age.json')
min_salary_with_max_age(database, 'min_salary_with_max_age.json')
age_stats_with_filter_by_salary(database, 'age_stats_with_filter_by_salary.json')
salary_stats_filter_by_city_job_age(database, 'salary_stats_filter_by_city_job_age.json')
salary_stats_filter_by_city(database, 'salary_stats_filter_by_city.json')
