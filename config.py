import os

from dotenv import load_dotenv


class Config:
    def __init__(self, env_file=".env"):
        """
        Initializes the Config object by loading environment
        variables from the .env file.
        """
        load_dotenv(env_file)
        self.__port = int(os.getenv("PORT", 5000))
        self.__kafka_conf = {
            "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            "client.id": os.getenv("KAFKA_CLIENT_ID", "mini-redis-app"),
        }
        self.__kafka_topic = os.getenv("KAFKA_TOPIC", "mini_redis_changes")
        self.__data_storage_file = os.getenv("DATA_STORAGE_FILE", "data.json")
        self.__update_message_broker = bool(os.getenv("UPDATE_MESSAGE_BROKER", False))
        self.__debug = bool(os.getenv("DEBUG", False))

    def get_port(self) -> int:
        """
        Gets the port number from the configuration.
        """
        return self.__port

    def get_kafka_conf(self) -> dict:
        """
        Gets the Kafka configuration dictionary.
        """
        return self.__kafka_conf

    def get_kafka_topic(self) -> str:
        """
        Gets the Kafka topic name where the latest shall be sent.
        """
        return self.__kafka_topic

    def get_data_storage_file(self) -> str:
        """
        Gets the file path for data storage.
        """
        return self.__data_storage_file

    def get_update_message_broker(self) -> bool:
        """
        Checks if message broker updates should be make.
        """
        return self.__update_message_broker

    def get_debug(self) -> bool:
        """
        Checks whether to run the server in DEBUG mode or not
        """
        return self.__debug
