from typing import Optional, Union
from typing_extensions import Annotated, Doc

from celery import Celery

from .._project_typing import BeatSchedule

__all__ = ["current_celery_app", "set_beat_schedule"]


def current_celery_app(
    app_name: str = __name__,
    *,
    broker_url: str,
    result_backend_url: str,
    include: Optional[list[str]] = None,
    **options,
):
    """
    current_celery_app _summary_

    Args:
        broker_url (str): _description_
        result_backend_url (str): _description_
        app_name (str, optional): _description_. Defaults to __name__.
        include (Optional[list[str]], optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    # from celery.events import EventReceiver

    return Celery(
        main=app_name,
        broker=broker_url,
        backend=result_backend_url,
        include=include,
        **options,
    )


def load_config_from_file(
    file_path: str,
) -> Union[BeatSchedule, dict[str, BeatSchedule], None]:
    from ._utils import load_file

    config = load_file(file_path)
    if config is None:
        return None
    if isinstance(config, list):
        raise TypeError("Config type must be a dictionary")
    return config


def set_beat_schedule_from_config(
    celery_app: Celery,
    beat_schedule: dict[str, BeatSchedule],
    dotkey: str,
) -> Celery:
    from ...collections import get_value_from_dotkey

    beat_schedule = get_value_from_dotkey(
        obj=beat_schedule,  # type: ignore
        dotkey=dotkey,
    )
    celery_app.conf.beat_schedule = beat_schedule

    return celery_app


def set_beat_schedule_from_beat_schedule(
    celery_app: Celery, beat_schedule: BeatSchedule
) -> Celery:
    celery_app.conf.beat_schedule = beat_schedule

    return celery_app


def set_beat_schedule(
    celery_app: Celery,
    obj_or_path: Annotated[
        Union[BeatSchedule, str],
        Doc(
            """
            傳入一個合法的celery beat schedule 格式的dict
            或者是帶有celery beat schedule 格式的dict 的 toml file or json file
            或者是傳入celery beat schedule 的python file path
            """
        ),
    ],
    dotkey: Optional[str] = None,
) -> Celery:
    if isinstance(obj_or_path, str):
        config = load_config_from_file(obj_or_path)

        if config is None:
            celery_app.config_from_object(obj_or_path)

            return celery_app
    else:
        return set_beat_schedule_from_beat_schedule(
            celery_app=celery_app,
            beat_schedule=obj_or_path,  # type: ignore
        )

    from ._check_type import check_is_beat_schedule

    if check_is_beat_schedule(config):
        raise TypeError("config type must be dictionary type'")

    if dotkey:
        return set_beat_schedule_from_config(
            celery_app=celery_app,
            beat_schedule=config,  # type: ignore
            dotkey=dotkey,
        )
    else:
        return set_beat_schedule_from_beat_schedule(
            celery_app=celery_app,
            beat_schedule=config,  # type: ignore
        )


# def set_beat_schedule(
#     celery_app: Celery,
#     obj_or_path: Annotated[
#         Union[BeatSchedule, str],
#         Doc(
#             """
#             傳入一個合法的celery beat schedule 格式的dict
#             或者是帶有celery beat schedule 格式的dict 的 toml file or json file
#             或者是傳入celery beat schedule 的python file path
#             """
#         ),
#     ],
#     dotkey: Optional[str] = None,
# ) -> Celery:

#     if isinstance(obj_or_path, str):
#         from ._utils import load_file

#         config = load_file(obj_or_path)

#         if config is None:
#             celery_app.config_from_object(obj_or_path)

#             return celery_app

#         if isinstance(config, list):
#             raise TypeError("config type must be dictionary type'")

#         if dotkey:
#             from ...collections import get_value_from_dotkey

#             beat_schedule = get_value_from_dotkey(obj=config, dotkey=dotkey)

#         else:
#             beat_schedule = config

#         from ._check_type import check_is_beat_schedule

#         if check_is_beat_schedule(beat_schedule) is False:
#             raise TypeError(f"'{type(beat_schedule) = }' must be BeatSchedule type")

#         celery_app.conf.beat_schedule = beat_schedule

#         return celery_app

#     elif isinstance(obj_or_path, dict):
#         celery_app.conf.beat_schedule = obj_or_path

#         return celery_app

#     raise TypeError("'obj_or_path' must be 'str' or 'BeatSchedule'")


# var: BeatSchedule = {
#     "task_name": {
#         "task": "234",
#         "schedule": "1",
#     },
#     "task2": {
#         "task": "234",
#         "schedule": "1",
#     },
# }
