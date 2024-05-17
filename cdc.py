import json
import logging

from bson import json_util

from data_flow.mq import publish_to_rabbitmq
from db.mongo import MongoDatabaseConnector

# Configure logging
logging.basicConfig(
    level = logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s"
)


def stream_process():
    try:
        client = MongoDatabaseConnector()
        db = client['scrabble']
        logging.info("Connected to MongoDB")

        changes = db.watch([{"$match": {"operationType": {"$in": ["insert"]}}}])
        for change in changes:
            data_type = change['ns']['coll']
            entry_id = str(change['fullDocument']['_id'])
            change['fullDocument'].pop('_id')
            change['fullDocument']['type'] = data_type
            change['fullDocument']['entry_id'] = entry_id

            data = json.dumps(change['fullDocument'], default = json_util.default)
            logging.info(f"Change detected ane serialized: {data}")

            publish_to_rabbitmq(queue_name = 'test_queue', data = data)
            logging.info("Published message to RabbitMQ")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    stream_process()
