from datetime import timedelta
from typing import Any, Literal, Optional, Union
from typing_extensions import TypedDict, Required, NotRequired

from celery.schedules import crontab
from pydantic import BaseModel


__all__ = [
    "RabbitMQBrokerUrlOptions",
    "RedisBrokerUrlOptions",
    "BeatSchedule",
    "BeatScheduleParam",
    "TaskReceivedEvent",
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


"""
{
    'type': 'task-received',          # 事件类型
    'timestamp': 1234567890.0,        # 事件发生的时间戳
    'hostname': 'example.com',        # 发生事件的主机名
    'pid': 12345,                      # 发生事件的进程 ID
    'clock': '14:30:00',               # 事件发生的时钟时间
    'utcoffset': '+0800',              # 事件发生时的 UTC 偏移量
    'uuid': '123e4567-e89b-12d3-a456-426614174000',  # 任务的唯一标识符
    'name': 'tasks.add',              # 任务的名称
    'args': (4, 5),                    # 任务的位置参数
    'kwargs': {'z': 6},                # 任务的关键字参数
    'retries': 0,                      # 任务已经重试的次数
    'eta': None,                       # 任务预计执行的时间
    'expires': None,                   # 任务的过期时间
    'requester': 'example_user'        # 请求任务的来源
}

"""


class TaskReceivedEvent(TypedDict, total=False):
    """
    Options BeatSchedule的option參數

    Args:
        * type (str, optional): 設置任務的優先級
        * timestamp: (float, optional): 設置任務的最大重試次數
        * hostname: (str, optional): 設置任務的執行超時時間
        * pid: (int, optional): 設置任務的軟執行超時時間
        * clock: (str, optional): 事件发生的时钟时间
        * utcoffset: (str, optional): 事件发生时的 UTC 偏移量
        * uuid: (str, optional): 任务的唯一标识符
        * name: (str, optional): 任务的名称
        * args: (uple[Any,...], optional): 任务的位置参数
        * kwargs: (dict[str, Any], optional): 任务的关键字参数
        * retries: (int, optional): 任务已经重试的次数
        * eta: (float, optional): 任务预计执行的时间
        * expires: (float, optional): 任务的过期时间
        * requester: (str, optional): 请求任务的来源
        
    ```python=
    >>> event = {
    'type': 'task-received',          # 事件类型
    'timestamp': 1234567890.0,        # 事件发生的时间戳
    'hostname': 'example.com',        # 发生事件的主机名
    'pid': 12345,                      # 发生事件的进程 ID
    'clock': '14:30:00',               # 事件发生的时钟时间
    'utcoffset': '+0800',              # 事件发生时的 UTC 偏移量
    'uuid': '123e4567-e89b-12d3-a456-426614174000',  # 任务的唯一标识符
    'name': 'tasks.add',              # 任务的名称
    'args': (4, 5),                    # 任务的位置参数
    'kwargs': {'z': 6},                # 任务的关键字参数
    'retries': 0,                      # 任务已经重试的次数
    'eta': None,                       # 任务预计执行的时间
    'expires': None,                   # 任务的过期时间
    'requester': 'example_user'        # 请求任务的来源
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
