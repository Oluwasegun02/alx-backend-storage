#!/usr/bin/env python3
""" Module for Redis db """
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
import functools


UnionOfTypes = Union[str, bytes, int, float]

def count_calls(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper
class Cache:
    """ Class for methods that operate a caching system """

    def __init__(self):
        """ Instance of the Redis db """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: UnionOfTypes) -> str:
        """
        Method takes a data argument and returns a string
        """
        self._key = str(uuid4())
        self._redis.set(self._key, data)
        return self._key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> UnionOfTypes:
        """
        Retrieves data stored in redis using a key
        converts the result/value back to the desired format
        """
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, value: str) -> str:
        """ get a string """
        return self.get(value, str)

    def get_int(self, value: str) -> int:
        """ get an int """
        return self.get(value, int)
