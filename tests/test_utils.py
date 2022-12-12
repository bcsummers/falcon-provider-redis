"""Test hooks feature of falcon_provider_redis module."""
# standard library
import os

# first-party
from falcon_provider_redis.utils import RedisClient, Singleton, redis_client

REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))


def test_utils_redis_client() -> None:
    """Testing utils stand-alone redis_client method"""
    client = redis_client(port=REDIS_PORT)
    key = 'utils_test_key'
    value = 'utils_test_value'
    result = client.set(key, value)
    assert result is True

    data = client.get(key)
    assert data.decode() == value


def test_utils_blocking_pool() -> None:
    """Testing utils RedisClient with blocking pool."""
    del Singleton._instances  # remove singleton instance for testing blocking
    Singleton._instances = {}  # pylint: disable=protected-access
    client = RedisClient(port=REDIS_PORT, blocking_pool=True).client

    key = 'utils_blocking_pool_key'
    value = 'utils_blocking_pool_value'
    result = client.set(key, value)
    assert result is True

    data = client.get(key)
    assert data.decode() == value
