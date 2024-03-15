from typing import Any, Optional

from celery import Celery
from celery.events.state import State

from .._project_typing import TaskReceivedEvent

__all__ = ["CeleryBaseEvent"]


class CeleryBaseEvent:
    def __init__(self, celery_app: Celery):
        self.__celery_app = celery_app

        self.__state: State = celery_app.events.State()
        self.__is_set_events:bool = False
        
    @property
    def set_event(self):
        return self.__is_set_events

    def get_task(self, event: TaskReceivedEvent) -> Any:
        self.__state.event(event)

        return self.__state.tasks.get(event["uuid"])

    def on_task_succeeded(self, event: TaskReceivedEvent) -> None:
        """
        @override function

        on_task_succeeded 任務完成時啟動

        Args:
            event (TaskReceivedEvent): celery的event

        Example Code

        ```python=
        from typing import override

        class CeleryTestEventClass(CeleryBaseEvent):
            ...
            @override
            def on_task_succeeded(self, event: TaskReceivedEvent) -> None:
                ...
        ```
        """

    def on_task_received(self, event: TaskReceivedEvent) -> None:
        """
        @override function

        on_task_received 任務啟動後時啟動

        Args:
            event (TaskReceivedEvent): celery的event

        Example Code

        ```python=
        from typing import override

        class CeleryTestEventClass(CeleryBaseEvent):
            ...
            @override
            def on_task_received(self, event: TaskReceivedEvent) -> None:
                ...
        ```
        """

    def on_task_started(self, event: TaskReceivedEvent) -> None:
        """
        @override function

        on_task_started 任務剛啟動時啟動

        Args:
            event (TaskReceivedEvent): celery的event

        Example Code

        ```python=
        from typing import override

        class CeleryTestEventClass(CeleryBaseEvent):
            ...
            @override
            def on_task_started(self, event: TaskReceivedEvent) -> None:
                ...
        ```
        """

    def on_task_failed(self, event: TaskReceivedEvent) -> None:
        """
        @override function

        on_task_failed 任務失敗時啟動

        Args:
            event (TaskReceivedEvent): celery的event

        Example Code

        ```python=
        from typing import override

        class CeleryTestEventClass(CeleryBaseEvent):
            ...
            @override
            def on_task_failed(self, event: TaskReceivedEvent) -> None:
                ...
        ```
        """

    def add_event(
        self,
        limit: Optional[int] = None,
        timeout: Optional[int] = None,
        wakeup: bool = True,
    ):
        """
        add_event _summary_

        Args:
            limit (Optional[int], optional): _description_. Defaults to None.
            timeout (Optional[int], optional): _description_. Defaults to None.
            wakeup (bool, optional): _description_. Defaults to True.
            
        
        Example Code    
        ```python=
        self.receiver = EventReceiver(self.connection, handlers={
            "task-received": state.receive_task_received,
            "task-accepted": state.receive_task_event,
            "task-succeeded": state.receive_task_event,
            "task-retried": state.receive_task_event,
            "task-failed": state.receive_task_event,
            "worker-online": state.receive_worker_event,
            "worker-offline": state.receive_worker_event,
            "worker-heartbeat": state.receive_heartbeat,
        })
        ```    
        """
        with self.__celery_app.connection() as connection:
            from celery.events import EventReceiver

            recv = EventReceiver(
                connection,
                handlers={
                    "task-succeeded": self.on_task_succeeded,
                    "task-received": self.on_task_received,
                    "task-started": self.on_task_started,
                    "task-failed": self.on_task_failed,
                    # '*': on_task_succeeded,
                },
            )
            recv.capture(limit=limit, timeout=timeout, wakeup=wakeup)
            self.__is_set_event = True

    def get_celery_app(self, auto_add_event: bool = False) -> Celery:
        if auto_add_event:
            self.add_event()

        return self.__celery_app
