from typing import Any, TypeVar, Union, Literal, Optional, Mapping, Collection

from .._project_typing import (
    RabbitMQBrokerUrlOptions,
    RedisBrokerUrlOptions,
    BeatScheduleParam,
    BeatSchedule,
    JSON,
)

VT = TypeVar("VT", Any, BeatScheduleParam)

__all__ = [
    "combined_broker_param_to_url",
    "load_toml_file",
    "load_json_file",
]


def load_file(
    path: str,
) -> Union[
    dict[str, Union[Any, BeatSchedule]],
    JSON,
    None,
]:
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


def csv_to_file(
    table: Union[list[list[str]], list[Mapping[str, str]]],
    filepath: str,
    encoding: str = "UTF-8",
    delimiter: str = ",",
    newline: str = "",
) -> None:
    fieldnames: Optional[Collection[str]] = (
        table[0].keys() if isinstance(table[0], dict) else None
    )

    with open(filepath, "w", encoding=encoding, newline=newline) as csv_file:
        if fieldnames:
            from csv import DictWriter

            writer = DictWriter(f=csv_file, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
        else:
            from csv import writer

            writer = writer(csvfile=csv_file, delimiter=delimiter)

        writer.writerows(table)  # type: ignore


def json_to_file(
    data: Union[JSON, str],
    filepath: str,
    encoding: str = "UTF-8",
    indent: int = 4,
) -> None:
    with open(filepath, "w", encoding=encoding) as json_file:
        from json import dump

        if isinstance(data, str):
            from json import loads

            data = loads(data)

        dump(data, json_file, indent=indent)


def toml_to_file(
    data: Union[Mapping[str, Any], str],
    filepath: str,
    encoding: str = "UTF-8",
) -> None:
    if isinstance(data, dict):
        from pytomlpp import dumps

        data = dumps(data)

        with open(filepath, "w", encoding=encoding) as toml_file_writer:
            toml_file_writer.write(data)


def obj_to_file(
    obj: Any,
    filepath: str,
    mode: Literal["csv", "json", "toml_file"],
) -> None:
    if mode == "csv":
        csv_to_file(table=obj, filepath=filepath)

    elif mode == "json":
        json_to_file(data=obj, filepath=filepath)

    elif mode == "toml_file":
        toml_to_file(data=obj, filepath=filepath)

    raise KeyError(
        f"your mode is '{mode}', the mode must be 'csv', 'json', 'toml_file' "
    )


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
