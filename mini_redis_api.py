from flask import request, jsonify, Blueprint
from marshmallow import ValidationError

from mini_redis import MiniRedis
from schemas import SetValueSchema, ExpireSchema


class RedisAPI:
    blueprint = Blueprint("mini_redis_api", __name__)
    redis = MiniRedis()

    @staticmethod
    @blueprint.route("/", methods=["POST"])
    def set_value():
        """
        Set a key-value pair
        ---
        parameters:
          - name: body
            in: body
            schema:
              type: object
              properties:
                key:
                  type: string
                value:
                  type: string
            required:
              - key
              - value
        responses:
          200:
            description: Value set successfully
        """
        try:
            data = request.json
            SetValueSchema().load(data)
            key = data["key"]
            value = data["value"]
            return RedisAPI.redis.set(key, value)
        except ValidationError as err:
            return jsonify(err.messages), 400

    @staticmethod
    @blueprint.route("/<key>", methods=["GET"])
    def get_value(key):
        """
        Get the value of a key
        ---
        parameters:
          - name: key
            in: path
            type: string
            required: true
        responses:
          200:
            description: The value of the key
            schema:
              type: string
              example: "name of person"
          404:
            description: The key is not set
            schema:
              type: string
              example: "Key not found"
        """
        value = RedisAPI.redis.get(key)
        if value is None:
            return jsonify("Key not found"), 404
        return jsonify(value)

    @staticmethod
    @blueprint.route("/<key>", methods=["DELETE"])
    def delete_value(key):
        """
        Delete a key-value pair
        ---
        parameters:
          - name: key
            in: path
            type: string
            required: true
        responses:
          200:
            description: Number of keys deleted
            schema:
              type: integer
              example: 1
        """
        deleted_keys = RedisAPI.redis.delete(key)
        return jsonify(deleted_keys)

    @staticmethod
    @blueprint.route("/expire", methods=["POST"])
    def expire_key():
        """
        Set an expiration on a key
        ---
        parameters:
          - name: body
            in: body
            schema:
              type: object
              properties:
                key:
                  type: string
                seconds:
                  type: integer
            required:
              - key
              - seconds
        responses:
          200:
            description: Expire set successfully
            schema:
              type: integer
              example: 1
        """
        try:
            data = request.json
            ExpireSchema().load(data)
            key = data["key"]
            seconds = int(data["seconds"])
            result = RedisAPI.redis.expire(key, seconds)
            return jsonify(result)
        except ValidationError as err:
            return jsonify(err.messages), 400

    @staticmethod
    @blueprint.route("/ttl/<key>", methods=["GET"])
    def ttl_key(key):
        """
        Get the time-to-live for a key
        ---
        parameters:
          - name: key
            in: path
            type: string
            required: true
        responses:
          200:
            description: Time-to-live in seconds
            schema:
              type: integer
              example: 42
        """
        result = RedisAPI.redis.ttl(key)
        return jsonify(result)
