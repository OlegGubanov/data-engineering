import csv
import json
import sqlite3


def connect_to_db(filename):
    connection = sqlite3.connect(filename)
    # connection.set_trace_callback(print)
    connection.row_factory = sqlite3.Row
    return connection


def read_users():
    users = []
    reader = csv.DictReader(open('users.csv'))
    for row in reader:
        user = {}
        pairs = row.items()
        for pair in pairs:
            user[pair[0]] = int(pair[1])
        users.append(user)
    return users


def insert_users(db, users):
    cursor = db.cursor()

    cursor.executemany("insert into users(user_id, products, reviews) values (:user_id, :products, :reviews)", users)
    db.commit()

    cursor.close()


def read_games():
    games = []
    reader = csv.DictReader(open('games.csv', encoding='utf-8'))
    for row in reader:
        game = {}
        pairs = row.items()
        for pair in pairs:
            key = pair[0]
            value = pair[1]
            if key in ['app_id', 'positive_ratio', 'user_reviews']:
                game[key] = int(value)
            elif key in ['title', 'date_release', 'rating']:
                game[key] = value
            elif key in ['win', 'mac', 'linux', 'steam_deck']:
                game[key] = value == 'true'
            elif key in ['price_final', 'price_original', 'discount']:
                game[key] = float(value)
        games.append(game)
    return games


def insert_games(db, games):
    cursor = db.cursor()

    cursor.executemany("""insert into games(app_id, title, date_release, win, mac, linux, rating, positive_ratio,
    user_reviews, price_final, price_original, discount, steam_deck) values (:app_id, :title, :date_release, :win,
    :mac, :linux, :rating, :positive_ratio, :user_reviews, :price_final, :price_original, :discount, :steam_deck)""",
    games)
    db.commit()

    cursor.close()


def read_metadata():
    data = []
    with open('games_metadata.json', mode='r', encoding='utf-8') as file:
        for line in file:
            metadata = json.loads(line)
            metadata['tags'] = json.dumps(metadata['tags'])
            data.append(metadata)
    return data


def insert_metadata(db, metadata):
    cursor = db.cursor()

    cursor.executemany("""insert into games_metadata(app_id, description, tags) 
    values (:app_id, :description, :tags)""", metadata)
    db.commit()

    cursor.close()


def write_data(filename, data):
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def query_1(db, filename):
    query = 'select * from users where products > 10000 order by products desc limit 100'
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    data = [dict(row) for row in result]
    cursor.close()

    write_data(filename, data)


def query_2(db, filename):
    query = 'select * from games where positive_ratio > 95 and user_reviews > 100000 order by title limit 100'
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    data = [dict(row) for row in result]
    cursor.close()

    write_data(filename, data)


def query_3(db, filename):
    query = 'select * from games where win == 1 and mac == 1 and linux == 1 and steam_deck == 1 order by title limit 100'
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    data = [dict(row) for row in result]
    cursor.close()

    write_data(filename, data)


def query_4(db, filename):
    query = """select games.title, games_metadata.description, games_metadata.tags 
    from games
    inner join games_metadata
    on games.app_id = games_metadata.app_id
    order by games.app_id"""
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    data = [dict(row) for row in result]
    cursor.close()

    write_data(filename, data)


def query_5(db, filename):
    query = """select sum(price_final) as sum, min(price_final) as min, 
    max(price_final) as max, avg(price_final) as avg from games"""
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    data = [dict(row) for row in result]
    cursor.close()

    write_data(filename, data)


def query_6(db, filename):
    query = """select rating, cast(count() as real) / (select count() from games) as count 
            from games group by rating order by count desc"""
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    data = [dict(row) for row in result]
    cursor.close()

    write_data(filename, data)


def query_7(db, filename):
    query = """select * from games where positive_ratio >= 95 and price_final = 0.0 order by title"""
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    data = [dict(row) for row in result]
    cursor.close()

    write_data(filename, data)


connection = connect_to_db('5_db')
# users = read_users()
# insert_users(connection, users)
# games = read_games()
# insert_games(connection, games)
# metadata = read_metadata()
# insert_metadata(connection, metadata)
query_1(connection, '100_users_with_more_than_10000_games.json')
query_2(connection, '100_games_with_very_positive_rating.json')
query_3(connection, '100_games_on_all_os.json')
query_4(connection, 'games_with_description_and_tags.json')
query_5(connection, 'price_stats.json')
query_6(connection, 'grouped_by_rating.json')
query_7(connection, 'free_games_with_very_positive_rating.json')
