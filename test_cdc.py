
from pymongo import MongoClient


def insert_data_to_mongodb(uri, database_name, collection_name, data):
    """
    Insert data into a MongoDB collection.

    :param uri: MongoDB URI
    :param database_name: Name of the database
    :param collection_name: Name of the collection
    :param data: Data to be inserted (dict)
    """
    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]

    try:
        result = collection.insert_one(data)
        print(f"Data inserted with _id: {result.inserted_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    # mongodb_uri = "mongodb://3.76.251.231:30001,3.76.251.231:30002,3.76.251.231:30003/?replicaSet=my-replica-set"
    # mongodb_uri = "mongodb://fmigas:fmigas123@3.76.251.231:27017"
    # mongodb_uri = "mongodb://3.76.251.231:27017"
    # mongodb_uri = "mongodb://3.76.251.231:27017/?replicaSet=my-replica-set"
    mongodb_uri = "mongodb://3.76.251.231:27017,3.76.251.231:27017,3.76.251.231:27017/?replicaSet=rs0"
    database_name = "franek"
    collection_name = "llm"
    test_data = {"name2": "coś tam nowego"}
    insert_data_to_mongodb(mongodb_uri, database_name, collection_name, test_data)
