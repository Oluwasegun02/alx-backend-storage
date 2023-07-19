#!/usr/bin/env python3
""" Module for Redis db """
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
import functools


UnionOfTypes = Union[str, bytes, int, float]

def call_history(method: Callable) -> Callable:
    """ call_history decorator to store the history of inputs and outputs for a particular function
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Append the input arguments as a normalized string to the input list 
        Execute the original method and store the output
        """

        key = method.__qualname__
        input_list_key = f"{key}:inputs"
        output_list_key = f"{key}:outputs"

        self._redis.rpush(input_list_key, str(args))

        output = method(self, *args, **kwargs)
        self._redis.rpush(output_list_key, str(output))

        # Return the output
        return output
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
