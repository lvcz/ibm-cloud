from pymongo import MongoClient
from os import environ
from uuid import uuid4
port = 27017


def create_new_link_model(current_link, status_code, links, father_url, error=None):
    conn = environ.get('MONGO_CONN')
    username = environ.get('MONGO_USERNAME')
    password = environ.get('MONGO_PASSWORD')
    client = MongoClient('mongodb://%s:%s@%s' % (username, password, conn))
    db = client.ibmscrap
    collection = db.link
    to_store = {
        'id': uuid4(),
        'current_link': current_link,
        'status_code': status_code,
        'error': error,
        'links': links,
        'father_url': father_url
    }
    collection.insert_one(to_store)
    client.close()
    return to_store.get('id')


def get_all_children(current_url):
    conn = environ.get('MONGO_CONN')
    username = environ.get('MONGO_USERNAME')
    password = environ.get('MONGO_PASSWORD')
    client = MongoClient('mongodb://%s:%s@%s' % (username, password, conn))
    db = client.ibmscrap
    collection = db.link
    result = collection.find({'father_url': current_url})
    client.close()
    return result


def get_my_node(current_link):
    conn = environ.get('MONGO_CONN')
    username = environ.get('MONGO_USERNAME')
    password = environ.get('MONGO_PASSWORD')
    client = MongoClient('mongodb://%s:%s@%s' % (username, password, conn))
    db = client.ibmscrap
    collection = db.link
    result = collection.find({'current_link': current_link})
    client.close()
    return result


def check_if_been_crawled(current_link):
    conn = environ.get('MONGO_CONN')
    username = environ.get('MONGO_USERNAME')
    password = environ.get('MONGO_PASSWORD')
    client = MongoClient('mongodb://%s:%s@%s' % (username, password, conn))
    db = client.ibmscrap
    collection = db.link
    result = collection.count_documents({'current_link': current_link})
    client.close()
    return result
