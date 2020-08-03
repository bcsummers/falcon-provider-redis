# -*- coding: utf-8 -*-
"""Falcon app used for testing."""
# standard library
import os

# third-party
import falcon
import redis

# first-party
from falcon_provider_redis.hooks import redis_client
from falcon_provider_redis.middleware import RedisMiddleware

# redis server
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))


class RedisHookResource:
    """Redis hook testing resource."""

    @falcon.before(redis_client, host=REDIS_HOST, port=REDIS_PORT)
    def on_get(
        self, req: falcon.Request, resp: falcon.Response,
    ):
        """Support GET method."""
        key: str = req.get_param('key')
        try:
            resp.body = self.redis_client.get(key)  # pylint: disable=no-member
            resp.status_code = falcon.HTTP_OK
        except redis.exceptions.RedisError:
            raise falcon.HTTPInternalServerError(
                code=1234,
                description='Unexpected error occurred while retrieving data.',
                title='Internal Server Error',
            )

    @falcon.before(redis_client, host=REDIS_HOST, port=REDIS_PORT)
    def on_post(
        self, req: falcon.Request, resp: falcon.Response,
    ):
        """Support POST method."""
        key: str = req.get_param('key')
        value: str = req.get_param('value')
        try:
            resp.body = str(self.redis_client.set(key, value))  # pylint: disable=no-member
            resp.status_code = falcon.HTTP_OK
        except redis.exceptions.RedisError:
            raise falcon.HTTPInternalServerError(
                code=1234,
                description='Unexpected error occurred while retrieving data.',
                title='Internal Server Error',
            )


app_hook = falcon.API()
app_hook.add_route('/hook', RedisHookResource())


class RedisMiddleWareResource:
    """Redis middleware testing resource."""

    def on_get(
        self, req: falcon.Request, resp: falcon.Response,
    ):
        """Support GET method."""
        key: str = req.get_param('key')
        try:
            resp.body = self.redis_client.get(key)  # pylint: disable=no-member
            resp.status_code = falcon.HTTP_OK
        except redis.exceptions.RedisError:
            raise falcon.HTTPInternalServerError(
                code=1234,
                description='Unexpected error occurred while retrieving data.',
                title='Internal Server Error',
            )

    def on_post(
        self, req: falcon.Request, resp: falcon.Response,
    ):
        """Support POST method."""
        key: str = req.get_param('key')
        value: str = req.get_param('value')
        try:
            resp.body = str(self.redis_client.set(key, value))  # pylint: disable=no-member
            resp.status_code = falcon.HTTP_OK
        except redis.exceptions.RedisError:
            raise falcon.HTTPInternalServerError(
                code=1234,
                description='Unexpected error occurred while retrieving data.',
                title='Internal Server Error',
            )


app_middleware = falcon.API(middleware=[RedisMiddleware(host=REDIS_HOST, port=REDIS_PORT)])
app_middleware.add_route('/middleware', RedisMiddleWareResource())
