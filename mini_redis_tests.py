import unittest
from mini_redis import MiniRedis


class TestMiniRedis(unittest.TestCase):
    def setUp(self):
        """
        Initializes a MiniRedis instance before each test.
        """
        self.redis = MiniRedis()

    def tearDown(self):
        """
        Deletes the MiniRedis instance after each test.
        """
        del self.redis

    def test_set_and_get(self):
        """
        Tests the 'set' and 'get' methods of the MiniRedis class.
        """
        self.redis.set("name", "Peter")
        self.assertEqual(self.redis.get("name"), "Peter")

    def test_delete(self):
        """
        Tests the 'delete' method of the MiniRedis class.
        """
        self.redis.set("name", "Jane")
        self.redis.delete("name")
        self.assertIsNone(self.redis.get("name"))

    def test_expire(self):
        """
        Tests the 'expire' method of the MiniRedis class.
        """
        self.redis.set("name", "John")
        self.redis.expire("name", 2)
        self.assertIsNotNone(self.redis.get("name"))
        import time

        time.sleep(3)
        self.assertIsNone(self.redis.get("name"))

    def test_ttl(self):
        """
        Tests the 'ttl' method of the MiniRedis class.
        """
        self.redis.set("name", "Winnie")
        self.assertEqual(self.redis.ttl("name"), -1)
        self.redis.expire("name", 5)
        self.assertGreaterEqual(self.redis.ttl("name"), 0)
        self.redis.delete("name")
        self.assertEqual(self.redis.ttl("name"), -2)


if __name__ == "__main__":
    unittest.main()
