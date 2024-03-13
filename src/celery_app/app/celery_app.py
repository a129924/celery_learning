from typing import Union, Optional
from typing_extensions import Self

from .._project_typing import RabbitMQBrokerUrlOptions, RedisBrokerUrlOptions


class CeleryApp:
    def __init__(
        self,
        broker_url_options: Union[RabbitMQBrokerUrlOptions, RedisBrokerUrlOptions],
        result_backed_url: str,
        include: Optional[list[str]] = None,
        **options,
    ):
        from ..utils import combined_broker_param_to_url, current_celery_app

        self.__celery_app = current_celery_app(
            app_name="demo",
            broker_url=combined_broker_param_to_url(broker_url_options),
            result_backend_url=result_backed_url,
            include=include,
            **options,
        )

    def get_celery_app(self):
        return self.__celery_app

    def set_config_from_object(self, object_path_or_object: Union[object, str]) -> Self:
        self.__celery_app.config_from_object(obj=object_path_or_object)
        self.__celery_app.conf.timezone

        return self

    def set_config_from_toml_file(
        self, toml_file_path: str, config_key: Optional[str] = None
    ) -> Self:
        from ..utils import load_toml_file
        
        config = load_toml_file(toml_file_path)

        self.__celery_app.config_from_object(
            obj=config[config_key]
            if config_key
            else config
        )

        return self
    
    def set_config_from_env(self,variable_name:str):
        self.__celery_app.config_from_envvar(variable_name)
        
        return self
