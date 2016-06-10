from redis import Redis, ConnectionPool

redis = Redis()


def configure_redis(app):
    connection_pool = ConnectionPool(
        host=app.config.get('REDIS_HOST', 'localhost'),
        port=app.config.get('REDIS_PORT', 6379),
        db=app.config.get('REDIS_DB', 0),
    )
    redis.connection_pool = connection_pool
