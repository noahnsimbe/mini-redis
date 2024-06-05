import json
import os
import threading
import time

from config import Config
from data_file_watcher import setup_data_file_monitoring

config = Config()


class MiniRedis:
    def __init__(self):
        self.data: dict[str, str] = {}  # Hash table to store key-value pairs
        self.timeouts: dict[
            str, int
        ] = {}  # Hash table to store key-expiration time pairs
        self.lock = threading.Lock()  # Lock for thread safety
        self.load_from_file()  # Loads data from file into memory
        self.auto_save_interval: int = 5  # Auto-save interval in seconds
        self.auto_save_thread = threading.Thread(
            target=self.auto_save
        )  # Auto-save thread
        self.auto_save_thread.daemon = True
        self.auto_save_thread.start()
        setup_data_file_monitoring()

    def set(self, key, value):
        """
        Sets the value associated with the given key.
        """
        with self.lock:
            self.data[key] = value
            self.timeouts.pop(key, None)
        return {key: value}

    def get(self, key) -> str:
        """
        Retrieves the value associated with the given key.
        """
        with self.lock:
            return self.data.get(key, None)

    def delete(self, key) -> int:
        """
        Deletes the key-value pair associated with the given key.
        """
        with self.lock:
            response = self.data.pop(key, 0)
            self.timeouts.pop(key, None)
            return response

    def expire(self, key, seconds) -> int:
        """
        Sets an expiration time (in seconds) for the given key.
        """
        with self.lock:
            if key in self.data:
                self.timeouts[key] = time.time() + seconds
                threading.Timer(seconds, self.delete, [key]).start()
                return 1
            return 0

    def ttl(self, key) -> int:
        """
        Returns the remaining time to live of the given key.
        """
        with self.lock:
            if key in self.data:
                if key in self.timeouts:
                    remaining = int(self.timeouts[key] - time.time())
                    return remaining if remaining > 0 else -1
                return -1
            return -2

    def save_to_file(self):
        """
        Saves the current data to the data storage file.
        """
        with self.lock:
            with open(config.get_data_storage_file(), "w") as f:
                json.dump(self.data, f)

    def load_from_file(self):
        """
        Loads data from the data storage file into memory.
        """
        if os.path.exists(config.get_data_storage_file()):
            with open(config.get_data_storage_file(), "r") as f:
                self.data = json.load(f)

    def auto_save(self):
        """
        Periodically saves data to the data storage file at a fixed interval.
        """
        while True:
            time.sleep(self.auto_save_interval)
            self.save_to_file()
