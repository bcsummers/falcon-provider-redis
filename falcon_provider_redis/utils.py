"""Redis client utility."""

# third-party
import redis


class Singleton(type):
    """A singleton Metaclass"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Evoke call method."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisClient(metaclass=Singleton):
    """A shared REDIS client connection using a ConnectionPooling singleton.

    Initialize a single shared redis.connection.ConnectionPool.

    For a full list of kwargs see https://redis-py.readthedocs.io/en/latest/#redis.Connection.

    Args:
        host: The REDIS host.
        port: The REDIS port.
        db: The REDIS db.
        blocking_pool: Use BlockingConnectionPool instead of ConnectionPool.
        errors (kwargs): The REDIS errors policy (e.g. strict).
        max_connections (kwargs): The maximum number of connections to REDIS.
        password (kwargs): The REDIS password.
        socket_timeout (kwargs): The REDIS socket timeout.
        timeout (kwargs): The REDIS Blocking Connection Pool timeout value.
    """

    def __init__(
        self,
        host: str | None = 'localhost',
        port: int | None = 6379,
        db: int | None = 0,
        blocking_pool: bool | None = False,
        **kwargs
    ):
        """Initialize class properties"""
        self._client = None
        pool = redis.ConnectionPool
        if blocking_pool:
            pool = redis.BlockingConnectionPool
        self.pool = pool(host=host, port=port, db=db, **kwargs)

    @property
    def client(self) -> object:
        """Return an instance of redis.client.Redis."""
        if self._client is None:
            self._client = redis.Redis(connection_pool=self.pool)
        return self._client


def redis_client(
    host: str | None = 'localhost', port: int | None = 6379, db: int | None = 0, **kwargs
) -> object:
    """Return an instance of redis.client.Redis.

    For a full list of kwargs see https://redis-py.readthedocs.io/en/latest/#redis.Redis.

    Args:
        host: The REDIS host.
        port: The REDIS port.
        db: The REDIS db.
        password (kwargs): The REDIS password.
        max_connections (kwargs): The maximum number of connections to REDIS.
        socket_timeout (kwargs): The REDIS socket timeout.
        unix_socket_path ( kwargs): The REDIS UNIX socket path.

    Returns:
        redis.client.Redis: An instance of REDIS client.
    """
    if kwargs.get('unix_socket_path') is not None:  # pragma: no cover
        # unix socket path doesn't require host or port
        return redis.Redis(None, None, db, **kwargs)
    return redis.Redis(host, port, db, **kwargs)
