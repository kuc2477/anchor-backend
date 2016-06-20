import time
from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine
from news.utils.logging import logger
from .redis import redis
from ..constants import (
    REDIS_COVER_START_CHANNEL,
    REDIS_COVER_SUCCESS_CHANNEL,
    REDIS_COVER_ERROR_CHANNEL,
    COVER_START,
    COVER_SUCCESS,
    COVER_ERROR,
)


class NotifierComponent(ApplicationSession):
    def notify_schedule_state(self, topic, schedule):
        if not schedule:
            logger.warning('[Notifier] Invalid schedule passed to notifier')
            return
        self._notify(topic, schedule.id, schedule.state)

    def _notify(self, topic, *args):
        logger.info(
            '[Notifier] Push message on {} to the router'
            .format(topic)
        )
        self.publish(topic, *args)

    def _get_schedule(self, message):
        from .schedules.models import Schedule
        id = int(message['data'])
        return Schedule.query.get(id)

    def _on_cover_start(self, message):
        schedule = self._get_schedule(message)
        self.notify_schedule_state(COVER_START, schedule)

    def _on_cover_success(self, message):
        schedule = self._get_schedule(message)
        self.notify_schedule_state(COVER_SUCCESS, schedule)

    def _on_cover_error(self, message):
        schedule = self._get_schedule(message)
        self.notify_schedule_state(COVER_ERROR, schedule)

    @coroutine
    def onJoin(self, details):
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(**{
            REDIS_COVER_START_CHANNEL: self._on_cover_start,
            REDIS_COVER_SUCCESS_CHANNEL: self._on_cover_success,
            REDIS_COVER_ERROR_CHANNEL: self._on_cover_error,
        })
        while True:
            self.pubsub.get_message()
            time.sleep(0.1)


# notifier component alias
notifier = NotifierComponent
