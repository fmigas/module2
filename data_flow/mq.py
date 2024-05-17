import pika

from settings import settings


class RabbitMQConnection:
    _instance = None

    def __new__(cls,
                host: str = None,
                port: int = None,
                username: str = None,
                password: str = None,
                virtual_host: str = "/"
                ):

        if cls._instance is None:
            cls._instance = super(RabbitMQConnection, cls).__new__(cls)
        else:
            return cls._instance

    def __init__(self,
                 host: str = None,
                 port: int = None,
                 username: str = None,
                 password: str = None,
                 virtual_host: str = "/",
                 fail_silently: bool = False,
                 **kwargs
                 ):
        self.host = host or settings.RABBITMQ_HOST
        self.port = port or settings.RABBITMQ_PORT
        self.username = username or settings.RABBITMQ_DEFAULT_USERNAME
        self.password = password or settings.RABBITMQ_DEFAULT_PASSWORD
        self.virtual_host = virtual_host
        self.fail_silently = fail_silently
        self._connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        if not self._connection:
            try:
                credentials = pika.PlainCredentials(self.username, self.password)
                parameters = pika.ConnectionParameters(host = self.host,
                                                       port = self.port,
                                                       virtual_host = self.virtual_host,
                                                       credentials = credentials)
                self._connection = pika.BlockingConnection(parameters)
            except pika.exceptions.AMQPConnectionError as e:
                print(f"Could not connect to RabbitMQ: {e}")
                if not self.fail_silently:
                    raise e

    def is_connected(self):
        return self._connection is not None and self._connection.is_open

    def get_channel(self):
        if self.is_connected():
            return self._connection.channel()

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            print("RabbitMQ connection closed")


def publish_to_rabbitmq(queue_name: str, data: str):
    try:
        rabbitmq_conn = RabbitMQConnection()

        with rabbitmq_conn as conn:
            channel = conn.get_channel()
            channel.queue_declare(queue = queue_name, durable = True)
            channel.basic_publish(exchange = "",
                                  routing_key = queue_name,
                                  body = data,
                                  properties = pika.BasicProperties(
                                      delivery_mode = 2  # make message persistent
                                  ))
            print(f"Published message to {queue_name}")

    except pika.exeptions.UnroutableError:
        print(f"Could not publish message to RabbitMQ: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    RabbitMQConnection.publish_to_rabbitmq("test_queue", "Hello, RabbitMQ!")
