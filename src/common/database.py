__author__ = 'Godfred Doe'

import pymongo


class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['crawler']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query).sort([("summedFrequency",-1)])

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
