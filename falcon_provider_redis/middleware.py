# -*- coding: utf-8 -*-
"""Falcon REDIS middleware module."""
# standard library
from typing import Optional

# third-party
import falcon
import redis

from .utils import RedisClient


class RedisMiddleware:
    """REDIS middleware module.

    For a full list of kwargs see https://redis-py.readthedocs.io/en/latest/#redis.Connection.

    Args:
        host: The REDIS host.
        port: The REDIS port.
        db: The REDIS db.
        blocking_pool: Use BlockingConnectionPool instead of ConnectionPool.
        errors (kwargs): The REDIS errors policy (e.g. strict).
        max_connections (kwargs): The maximum number of connections to REDIS.
        password (kwargs): The REDIS password.
        redis_client (kwargs): An instance of REDIS client to use instead
            of built-in instance.
        socket_timeout (kwargs): The REDIS socket timeout.
        timeout (kwargs): The REDIS Blocking Connection Pool timeout value.
    """

    def __init__(
        self,
        host: Optional[str] = 'localhost',
        port: Optional[int] = 6379,
        db: Optional[int] = 0,
        **kwargs
    ):
        """Initialize class properties."""
        redis_client: redis.client.Redis = kwargs.get('redis_client')
        if not isinstance(redis_client, redis.client.Redis):
            redis_client = RedisClient(host, port, db, **kwargs).client
        self.redis_client = redis_client

    def process_resource(
        self, req: falcon.Request, resp: falcon.Response, resource: object, params: dict
    ):  # pylint: disable=unused-argument
        """Process resource method.

        .. code-block:: python
            :linenos:
            :lineno-start: 1

            def on_get(self, req, resp):
                try:
                    data = self.redis_client.get('foo')
                except redis.exceptions.RedisError:
                    raise falcon.HTTPInternalServerError(
                        code=self.code(),
                        description='Unexpected error occurred while retrieving data.',
                        title='Internal Server Error',
                    )
        """
        resource.redis_client = self.redis_client
