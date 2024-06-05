import json

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from config import Config
from message_broker import KafkaBroker

config = Config()


class DataFileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        """
        Overrides the on_modified method of FileSystemEventHandler.

        Reads the contents of the redis data storage file and
        sends them to the Kafka broker if sending to Kafka is enabled.
        """
        if config.get_update_message_broker():
            with open(config.get_data_storage_file(), "r") as f:
                data = json.load(f)
                kafka_broker = KafkaBroker()
                kafka_broker.send_to_message_broker(data)


def setup_data_file_monitoring():
    """
    Sets up file monitoring using the Observer pattern
    for the redis data storage file.
    """

    event_handler = DataFileEventHandler()
    observer = Observer()
    observer.schedule(
        event_handler, path=f"./{config.get_data_storage_file()}", recursive=False
    )
    observer.start()
