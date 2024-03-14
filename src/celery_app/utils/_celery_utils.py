from typing import Optional, Union
from typing_extensions import Annotated, Doc

from celery import Celery

from .._project_typing import BeatSchedule, JSON

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
        from ._utils import load_file

        config: Union[JSON, dict[str, BeatSchedule], None] = load_file(obj_or_path)

        if config is None:
            celery_app.config_from_object(obj_or_path)

            return celery_app

        if isinstance(config, list):
            raise TypeError("config type must be dictionary type'")

        from ._check_type import check_is_beat_schedule

        if check_is_beat_schedule(config):
            if dotkey:
                from ...collections import get_value_from_dotkey

                beat_schedule = get_value_from_dotkey(obj=config, dotkey=dotkey)

            else:
                beat_schedule = config

        else:
            raise TypeError("config must be BeatSchedule type")

        celery_app.conf.beat_schedule = beat_schedule

        return celery_app

    elif isinstance(obj_or_path, dict):
        celery_app.conf.beat_schedule = obj_or_path

        return celery_app


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
