from typing import Literal 
from typing_extensions import TypedDict, Required

__all__ = ["RabbitMQBrokerUrlOptions", "RedisBrokerUrlOptions"]

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