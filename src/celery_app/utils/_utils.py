from typing import Union


from celery_app._project_typing import RabbitMQBrokerUrlOptions, RedisBrokerUrlOptions

__all__ = ["combined_broker_param_to_url", "load_toml_file"]


def load_toml_file(path: str):
    from pytomlpp import load

    return load(path)


def combined_broker_param_to_url(
    broker_param: Union[RabbitMQBrokerUrlOptions, RedisBrokerUrlOptions],
) -> str:
    broker_mode = broker_param["broker_mode"]

    if broker_mode == "rabbitmq":
        if broker_param.get("vhost", None):
            return f"amqp://{broker_param['username']}:{broker_param['password']}@{broker_param['hostname']}:{broker_param['port']}/{broker_param['vhost']}"  # type: ignore

        else:
            return f"amqp://{broker_param['username']}:{broker_param['password']}@{broker_param['hostname']}:{broker_param['port']}"

    elif broker_mode == "redis":
        return f"redis://:{broker_param['password']}@{broker_param['hostname']}:{broker_param['port']}/{broker_param['db_number']}"  # type: ignore

    raise KeyError(f"'{broker_mode = }' must be 'rabbitmq' or 'redis'")


def current_celery_app(
    app_name: str = __name__,
    *,
    broker_url: str,
    result_backend_url: str,
    include: list[str],
    **options,
):
    from celery import Celery
    from celery.events import EventReceiver

    return Celery(
        main=app_name, broker=broker_url, backend=result_backend_url, **options
    )
