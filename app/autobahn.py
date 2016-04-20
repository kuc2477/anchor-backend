from flask import current_app
from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine
from .constants import (
    REDIS_COVER_FINISHED_CHANNEL,
    REDIS_COVER_START_CHANNEL,
    TOPIC_COVER_STARTED,
    TOPIC_COVER_FINISHED,
)
from .extensions import redis


# create app to make sure all app extensions are configured properly
if not current_app:
    from app import create_app_from_env
    create_app_from_env()


class NotifierComponent(ApplicationSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis = redis
        self.pubsub = redis.pubsub()

    def notify(self, topic, message):
        self.publish(topic, message)

    @coroutine
    def onJoin(self, details):
        self.pubsub.subscribe(**{
            REDIS_COVER_START_CHANNEL: lambda message:
            self.notify(TOPIC_COVER_STARTED, message),
            REDIS_COVER_FINISHED_CHANNEL: lambda message:
            self.notify(TOPIC_COVER_FINISHED, message)
        })
        self.thread = self.pubsub.run_in_thread()
