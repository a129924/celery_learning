from datetime import timedelta
from typing import Any, Literal, Mapping, Optional, Union
from typing_extensions import TypedDict, Required, NotRequired

from celery.schedules import crontab
from pydantic import BaseModel


__all__ = [
    "RabbitMQBrokerUrlOptions",
    "RedisBrokerUrlOptions",
    "BeatSchedule",
    "BeatScheduleParam",
    "TaskReceivedEvent",
    "EventByEventFucntion",
    "Options",
    "EventsParam",
]


class CeleryBrokerOptions(TypedDict):
    username: str
    password: str
    hostname: str
    port: int


class RabbitMQBrokerUrlOptions(CeleryBrokerOptions, total=False):
    broker_mode: Required[Literal["rabbitmq"]]
    vhost: str


class RedisBrokerUrlOptions(CeleryBrokerOptions):
    broker_mode: Literal["redis"]
    db_number: int


class Options(TypedDict, total=False):
    """
    Options BeatSchedule的option參數

    Args:
        * priority (int, optional): 設置任務的優先級
        * max_retries: (int, optional): 設置任務的最大重試次數
        * time_limit: (int, optional): 設置任務的執行超時時間
        * soft_time_limit: (int, optional): 設置任務的軟執行超時時間
    """

    priority: int
    max_retries: int
    time_limit: int
    soft_time_limit: int


class BeatScheduleParam(BaseModel):
    task: str
    schedule: Union[str, timedelta, crontab, int, float]
    args: Optional[tuple[Any, ...]] = None
    kwargs: Optional[dict[str, Any]] = None
    options: Optional[Options] = None


BeatSchedule = dict[
    str,  # task_name
    BeatScheduleParam,  # beat_schedule_param
]


class TaskReceivedEvent(TypedDict, total=False):
    """
    Options BeatSchedule的option參數

    Args:
        * type (str, optional): 設置任務的優先級
        * timestamp: (float, optional): 設置任務的最大重試次數
        * hostname: (str, optional): 設置任務的執行超時時間
        * pid: (int, optional): 設置任務的軟執行超時時間
        * clock: (str, optional): 事件發生的時鐘時間
        * utcoffset: (str, optional): 事件發生時的 UTC 偏移量
        * uuid: (str, optional): 任務的唯一標識符
        * name: (str, optional): 任務的名稱
        * args: (uple[Any,...], optional): 任務的位置參數
        * kwargs: (dict[str, Any], optional): 任務的關鍵字參數
        * retries: (int, optional): 任務已經重試的次數
        * eta: (float, optional): 任務預計執行的時間
        * expires: (float, optional): 任務的過期時間
        * requester: (str, optional): 請求任務的來源

    ```python=
        >>> event = {
        'type': 'task-received', # 事件類型
        'timestamp': 1234567890.0, # 事件發生的時間戳
        'hostname': 'example.com', # 發生事件的主機名
        'pid': 12345, # 發生事件的進程 ID
        'clock': '14:30:00', # 事件發生的時鐘時間
        'utcoffset': '+0800', # 事件發生時的 UTC 偏移量
        'uuid': '123e4567-e89b-12d3-a456-426614174000', # 任務的唯一標識符
        'name': 'tasks.add', # 任務的名稱
        'args': (4, 5), # 任務的位置參數
        'kwargs': {'z': 6}, # 任務的關鍵字參數
        'retries': 0, # 任務已經重試的次數
        'eta': None, # 任務預計執行的時間
        'expires': None, # 任務的過期時間
        'requester': 'example_user' # 請求任務的來源
        }
     ```

    """

    type: Required[str]
    timestamp: Required[float]
    hostname: Required[str]
    pid: Required[int]
    clock: Required[str]
    utcoffset: Required[str]
    uuid: Required[str]
    name: Required[str]
    retries: Required[int]
    args: NotRequired[Optional[tuple[Any, ...]]]
    kwargs: NotRequired[Optional[dict[str, Any]]]
    eta: NotRequired[Optional[float]]
    expires: NotRequired[Optional[float]]
    requester: NotRequired[Optional[str]]


EventByEventFucntion = Mapping[
    Literal["task-succeeded", "task-received", "task-started", "task-failed"],  # event
    str,  # event function
]


class EventsParam(TypedDict, total=False):
    limit: Optional[int]
    timeout: Optional[int]
    wakeup: bool
