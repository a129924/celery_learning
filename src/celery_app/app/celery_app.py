from typing import Union

from .._project_typing import RabbitMQBrokerUrlOptions, RedisBrokerUrlOptions


class CeleryApp:
    def __init__(
        self, broker_url_options: Union[RabbitMQBrokerUrlOptions, RedisBrokerUrlOptions]
    ):
        self.__celery_app = ...
