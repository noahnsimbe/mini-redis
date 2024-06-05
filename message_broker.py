import json
import time

from confluent_kafka import Producer

from config import Config

config = Config()


class KafkaBroker:
    def __init__(self):
        self.producer = Producer(config.get_kafka_conf())

    def send_to_message_broker(self, data):
        """
        Produces the messages to Kafka topic using
        current time (milliseconds) as the message key

        The message value is the JSON serialized redis data
        """
        self.producer.produce(
            config.get_kafka_topic(),
            key=str(int(time.time() * 1000)),
            value=json.dumps(data),
        )
        self.producer.flush()
