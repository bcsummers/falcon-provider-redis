# -*- coding: utf-8 -*-
"""Falcon REDIS hook module."""
# standard library
from typing import Optional

# third-party
import falcon

from .utils import RedisClient


def redis_client(
    req: falcon.Request,
    resp: falcon.Response,
    resource: object,
    params: dict,
    host: Optional[str] = None,
    port: Optional[int] = None,
    db: Optional[int] = None,
    **kwargs
):  # pylint: disable=unused-argument
    """Provide an instance of REDIS client to method via resource.

    .. note:: RedisClient is a singleton instance and therefore only needs the connection parameters
        provided once. It would be a best practice to establish the instance prior to using the hook
        so that the connection parameters are not required in the setup of the hook.

    .. code-block:: python
        :linenos:
        :lineno-start: 1

        @falcon.before(redis_client)
        def on_get(self, req, resp):
            try:
                data = self.redis_client.get('foo')
            except redis.exceptions.RedisError:
                raise falcon.HTTPInternalServerError(
                    code=self.code(),
                    description='Unexpected error occurred while retrieving data.',
                    title='Internal Server Error',
                )

    Args:
        req: The falcon req object.
        resp: The falcon resp object.
        resource: The falcon resp object.
        params: List of query params.
        host: The REDIS host.
        port: The REDIS port.
        db: The REDIS db.
    """
    resource.redis_client = RedisClient(host, port, db, **kwargs).client
