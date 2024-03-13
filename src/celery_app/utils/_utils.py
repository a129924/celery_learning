from typing import Any, TypeVar, Union


from .._project_typing import (
    RabbitMQBrokerUrlOptions,
    RedisBrokerUrlOptions,
    JSON,
    BeatScheduleParam,
    BeatSchedule,
)

VT = TypeVar("VT", Any, BeatScheduleParam)

__all__ = [
    "combined_broker_param_to_url",
    "load_toml_file",
    "load_json_file",
]


def load_file(
    path: str,
) -> Union[dict[str, Union[Any, BeatSchedule]], JSON, None]:
    if path.endswith(".json"):
        return load_json_file(path)
    elif path.endswith(".toml"):
        return load_toml_file(path)

    return None


def load_toml_file(path: str) -> dict[str, Any]:
    try:
        from pytomlpp import load
    except ImportError:
        print("can't not find 'pytomllpp.load' package")

    return load(path)


def load_json_file(path: str) -> JSON:
    with open(path) as json_file:
        from json import load

        return load(json_file)


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
