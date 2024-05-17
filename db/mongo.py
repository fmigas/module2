from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from settings import settings


class MongoDatabaseConnector:
    _instance: MongoClient = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = MongoClient(settings.MONGO_DATABASE_HOST)
            except ConnectionFailure as e:
                print(f"Could not connect to MongoDB: {e}")
                raise

        return cls._instance

    def get_database(self):
        return self._instance[settings.MONGO_DATABASE_NAME]

    def close(self):
        if self._instance:
            self._instance.close()


connection = MongoDatabaseConnector()
