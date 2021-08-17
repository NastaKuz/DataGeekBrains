from pymongo import MongoClient, errors


def insert_news(result):
    client = MongoClient('127.0.0.1', 27017)
    db = client['news']
    for item in result:
        try:
            db.news.insert_one(item)
        except errors.DuplicateKeyError:
            print("Новость уже есть в базе")
