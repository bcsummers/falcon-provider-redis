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
        self,
        req: falcon.Request,
        resp: falcon.Response,
    ):
        """Support GET method."""
        key: str = req.get_param('key')
        try:
            resp.text = self.redis_client.get(key)  # pylint: disable=no-member
            resp.status_code = falcon.HTTP_OK
        except redis.exceptions.RedisError as ex:
            raise falcon.HTTPInternalServerError(
                code=1234,
                description='Unexpected error occurred while retrieving data.',
                title='Internal Server Error',
            ) from ex

    @falcon.before(redis_client, host=REDIS_HOST, port=REDIS_PORT)
    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response,
    ):
        """Support POST method."""
        key: str = req.get_param('key')
        value: str = req.get_param('value')
        try:
            resp.text = str(self.redis_client.set(key, value))  # pylint: disable=no-member
            resp.status_code = falcon.HTTP_OK
        except redis.exceptions.RedisError as ex:
            raise falcon.HTTPInternalServerError(
                code=1234,
                description='Unexpected error occurred while retrieving data.',
                title='Internal Server Error',
            ) from ex


app_hook = falcon.App()
app_hook.add_route('/hook', RedisHookResource())


class RedisMiddleWareResource:
    """Redis middleware testing resource."""

    def on_get(
        self,
        req: falcon.Request,
        resp: falcon.Response,
    ):
        """Support GET method."""
        key: str = req.get_param('key')
        try:
            resp.text = self.redis_client.get(key)  # pylint: disable=no-member
            resp.status_code = falcon.HTTP_OK
        except redis.exceptions.RedisError as ex:
            raise falcon.HTTPInternalServerError(
                code=1234,
                description='Unexpected error occurred while retrieving data.',
                title='Internal Server Error',
            ) from ex

    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response,
    ):
        """Support POST method."""
        key: str = req.get_param('key')
        value: str = req.get_param('value')
        try:
            resp.text = str(self.redis_client.set(key, value))  # pylint: disable=no-member
            resp.status_code = falcon.HTTP_OK
        except redis.exceptions.RedisError as ex:
            raise falcon.HTTPInternalServerError(
                code=1234,
                description='Unexpected error occurred while retrieving data.',
                title='Internal Server Error',
            ) from ex


app_middleware = falcon.App(middleware=[RedisMiddleware(host=REDIS_HOST, port=REDIS_PORT)])
app_middleware.add_route('/middleware', RedisMiddleWareResource())
