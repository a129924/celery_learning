from typing import Any, Union

from .._project_typing import BeatScheduleParam, BeatSchedule


__all__ = ["check_is_beat_schedule"]


def check_is_beat_schedule_param(obj: Union[Any, BeatScheduleParam]) -> bool:
    return isinstance(obj, BeatScheduleParam)


def check_is_beat_schedule(config: Union[Any, BeatSchedule]) -> bool:
    if not isinstance(config, dict):
        return False

    for key, value in config.items():
        if not isinstance(key, str) or not isinstance(value, BeatScheduleParam):
            return False

    return True
