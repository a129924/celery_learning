from typing import Any, Optional

from celery import Celery
from celery.events.state import State

from .._project_typing import TaskReceivedEvent


class CeleryEvent:
    def __init__(self, celery_app: Celery):
        self.__celery_app = celery_app

        self.__state: State = celery_app.events.State()

    def get_task(self, event: TaskReceivedEvent) -> Any:
        self.__state.event(event)

        return self.__state.tasks.get(event["uuid"])

    def on_task_succeeded(self, event: TaskReceivedEvent):
        ...

    def get_celery_app(
        self,
    ) -> Celery:
        return self.__celery_app
