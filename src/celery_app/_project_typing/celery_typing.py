from datetime import timedelta
from typing import Any, Literal , Union
from typing_extensions import TypedDict, Required

from celery.schedules import crontab


__all__ = ["RabbitMQBrokerUrlOptions", "RedisBrokerUrlOptions", "BeatSchedule","BeatScheduleParam"]

class CeleryBrokerOptions(TypedDict):
    username:str
    password:str
    hostname:str
    port:int


class RabbitMQBrokerUrlOptions(CeleryBrokerOptions, total=False):
    broker_mode:Required[Literal['rabbitmq']]
    vhost:str
    
class RedisBrokerUrlOptions(CeleryBrokerOptions):
    broker_mode:Literal['redis']
    db_number:int

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
    
class BeatScheduleParam(TypedDict, total=False):
    task: Required[str]
    schedule : Required[Union[str, timedelta,crontab, int, float]]
    args : tuple[Any, ...]
    kwargs : dict[str, Any]
    options : Options

BeatSchedule = dict[
    str, # task_name
    BeatScheduleParam # beat_schedule_param
]