=====================
falcon-provider-redis
=====================

|build| |coverage| |code-style| |pre-commit|

A falcon hook and middleware provider for Redis.

------------
Installation
------------

Install the extension via pip.

.. code:: bash

    > pip install falcon-provider-redis

--------
Overview
--------

This package provides a hook and middleware component for the falcon framework via the RedisClient class in utils.py. This class is a Singleton that uses a connection pool for the Redis client.  The RedisClient class can also be accessed directly outside of the hook or middleware if required.  There is also a stand-alone ``redis_client`` method that provides a single client connection to Redis.

--------
Requires
--------
* falcon - https://pypi.org/project/falcon/
* hiredis - https://pypi.org/project/hiredis/
* redis - https://pypi.org/project/redis/

----
Hook
----

The redis_client hook can be applied at the class level or the method level. If applied at the class level each responder method will have access to ``self.redis_client`` (an instance of redis.client.Redis) or if applied at the method level that method will have access to ``self.redis_client``. For more information on falcon hooks see https://falcon.readthedocs.io/en/stable/api/hooks.html and for more information on Redis client methods see https://redis.io/commands.

.. code:: python

    import os
    import falcon
    import redis
    from falcon_provider_redis.hooks import redis_client

    # redis server
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))

    class RedisHookResource(object):
        """Redis hook testing resource."""

        @falcon.before(redis_client, host=REDIS_HOST, port=REDIS_PORT)
        def on_get(self, req, resp):
            key = req.get_params('key')
            try:
                data = self.redis_client.get(key)
            except redis.exceptions.RedisError:
                raise falcon.HTTPInternalServerError(
                    code=self.code(),
                    description='Unexpected error occurred while retrieving data.',
                    title='Internal Server Error',
                )

    app_middleware = falcon.App()
    app_middleware.add_route('/hook', RedisHookResource()

----------
Middleware
----------

When using RedisMiddleWare all responder methods will have access to ``self.redis_client`` (an instance of redis.client.Redis). For more information on falcon middleware see https://falcon.readthedocs.io/en/stable/api/middleware.html and for more information on Redis client methods see https://redis.io/commands.

.. code:: python

    import os
    import falcon
    import redis
    from falcon_provider_redis.middleware import RedisMiddleware

    # redis server
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))

    class RedisMiddleWareResource(object):
        """Redis middleware testing resource."""

        def on_get(self, req, resp):
            """Support GET method."""
            key = req.get_param('key')
            try:
                resp.text = self.redis_client.get(key)
                resp.status_code = falcon.HTTP_OK
            except redis.exceptions.RedisError:
                raise falcon.HTTPInternalServerError(
                    code=1234,
                    description='Unexpected error occurred while retrieving data.',
                    title='Internal Server Error',
                )

    app_middleware = falcon.App(middleware=[RedisMiddleware(host=REDIS_HOST, port=REDIS_PORT)])

    app_middleware.add_route('/middleware', RedisMiddleWareResource()

-----------
Development
-----------

Installation
------------

After cloning the repository, all development requirements can be installed via pip. For linting and code consistency the pre-commit hooks should be installed.

.. code:: bash

    > poetry install --with dev
    > pre-commit install

Testing
-------

.. code:: bash

    > poetry install --with dev,test
    > pytest --cov=falcon_provider_redis --cov-report=term-missing tests/

.. |build| image:: https://github.com/bcsummers/falcon-provider-redis/workflows/build/badge.svg
    :target: https://github.com/bcsummers/falcon-provider-redis/actions

.. |coverage| image:: https://codecov.io/gh/bcsummers/falcon-provider-redis/branch/master/graph/badge.svg?token=prpmecioDm
    :target: https://codecov.io/gh/bcsummers/falcon-provider-redis

.. |code-style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black

.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
