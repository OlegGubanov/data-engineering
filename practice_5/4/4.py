import json
import pickle
from pymongo import MongoClient
from bson.json_util import dumps


def load_data_json():
    with open('27.json', mode='r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def load_data_pickle():
    with open('44.pkl', mode='br') as file:
        data = pickle.load(file)
        return data


def connect_to_database():
    client = MongoClient()
    db = client["football-database"]
    return db.matches


def insert_data(db, data):
    db.insert_many(data)


def write_data(filename, data):
    with open(filename, mode='w', encoding='utf-8') as file:
        file.write(data)


data_1 = load_data_json()
data_2 = load_data_pickle()
db = connect_to_database()
# insert_data(db, data_1)
# insert_data(db, data_2)


def sort_by_home_score(db, filename):
    cursor = db.find(limit=10).sort({'home_score': -1})
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def filter_by_home_team_name(db, filename):
    cursor = db.find({"home_team.home_team_name": "Arsenal"}).sort({'match_week': 1})
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def filter_by_time(db, filename):
    cursor = db.find({"kick_off": {"$gt": "20:00:00.000"}}).sort({'kick_off': -1})
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def filter_by_score(db, filename):
    cursor = db.find({"home_score": 0, "away_score": 0}).sort({'match_week': 1})
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def matches_by_referee(db, filename):
    cursor = db.count_documents({"referee.name": "Mark Clattenburg"})
    data = {"count": cursor}
    write_data(filename, json.dumps(data, indent=4))


# sort_by_home_score(db, 'sort_by_home_score.json')
# filter_by_home_team_name(db, 'filter_by_home_team_name.json')
# filter_by_time(db, 'filter_by_time.json')
# filter_by_score(db, 'filter_by_score.json')
# matches_by_referee(db, 'matches_by_referee.json')


def stats_by_home_score(db, filename):
    query = [
        {
            "$group": {
                "_id": None,
                "min": {"$min": "$home_score"},
                "avg": {"$avg": "$home_score"},
                "max": {"$max": "$home_score"}
            }
        }
    ]

    cursor = db.aggregate(query)
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def stats_by_away_score_filter_by_team(db, filename):
    query = [
        {
            "$match": {
                "away_team.away_team_name": "Arsenal"
            }
        },
        {
            "$group": {
                "_id": None,
                "min": {"$min": "$away_score"},
                "avg": {"$avg": "$away_score"},
                "max": {"$max": "$away_score"}
            }
        }
    ]

    cursor = db.aggregate(query)
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def stats_by_match_week_filter_by_referee(db, filename):
    query = [
        {
            "$match": {
                "referee.name": "Martin Atkinson"
            }
        },
        {
            "$group": {
                "_id": None,
                "min": {"$min": "$match_week"},
                "avg": {"$avg": "$match_week"},
                "max": {"$max": "$match_week"}
            }
        }
    ]

    cursor = db.aggregate(query)
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def stats_by_home_score_filter_by_referee_and_team(db, filename):
    query = [
        {
            "$match": {
                "referee.name": "Craig Pawson",
                "home_team.home_team_name": "Leicester City"
            }
        },
        {
            "$group": {
                "_id": None,
                "min": {"$min": "$home_score"},
                "avg": {"$avg": "$home_score"},
                "max": {"$max": "$home_score"}
            }
        }
    ]

    cursor = db.aggregate(query)
    data = dumps(list(cursor), indent=4, ensure_ascii=False)
    write_data(filename, data)


def stats_by_home_score_group_by_team_filter_by_competition(db, filename):
    query = [
        {
            "$match": {
                "competition.competition_name": "Premier League"
            }
        },
        {
            "$group": {
                "_id": "$home_team.home_team_name",
                "min": {"$min": "$home_score"},
                "avg": {"$avg": "$home_score"},
                "max": {"$max": "$home_score"}
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


# stats_by_home_score(db, 'stats_by_home_score.json')
# stats_by_away_score_filter_by_team(db, 'stats_by_away_score_filter_by_team.json')
# stats_by_match_week_filter_by_referee(db, 'stats_by_match_week_filter_by_referee.json')
# stats_by_home_score_filter_by_referee_and_team(db, 'stats_by_home_score_filter_by_referee_and_team.json')
# stats_by_home_score_group_by_team_filter_by_competition(db, 'stats_by_home_score_group_by_team.json')

def delete_by_score(db):
    result = db.delete_many({
        "$and": [
            {"home_score": 0},
            {"away_score": 0}
        ]
    })

    print(result)


def delete_by_kickoff(db):
    result = db.delete_many({
        "kick_off": {"$lt": "14:00:00.000"}
    })

    print(result)


def update_data_version(db):
    update = {
        "$set": {
            "metadata.data_version": "1.1.1"
        }
    }

    result = db.update_many({}, update)
    print(result)


def update_home_score_filter_by_team(db):
    filter = {
        "home_team.home_team_name": "Arsenal"
    }

    update = {
        "$inc": {
            "home_score": 1
        }
    }

    result = db.update_many(filter, update)
    print(result)


def delete_draws(db):
    filter = {
        "$expr": {
            "$eq": ["$home_score", "$away_score"]
        }
    }

    result = db.delete_many(filter)
    print(result)


# delete_by_score(db)
# delete_by_kickoff(db)
# update_data_version(db)
# update_home_score_filter_by_team(db)
# delete_draws(db)
