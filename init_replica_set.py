from pymongo import MongoClient
import time

# Connect to the primary MongoDB instance
client = MongoClient('mongodb://3.76.251.231:30001/')

# Wait for the replica set to be initialized
while True:
    try:
        config = client.admin.command('replSetGetConfig')
        break
    except Exception as e:
        print(f"Waiting for replica set to be initialized... ({e})")
        time.sleep(5)

# Initialize the replica set
client.admin.command('replSetInitiate', {
    '_id': 'my-replica-set',
    'members': [
        {'_id': 0, 'host': '3.76.251.231:30001'},
        {'_id': 1, 'host': '3.76.251.231:30002'},
        {'_id': 2, 'host': '3.76.251.231:30003'}
    ]
})

print('Replica set initialized successfully.')
