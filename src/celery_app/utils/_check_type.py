from typing import Any, Union

from .._project_typing import BeatScheduleParam, BeatSchedule


__all__ = ["check_is_beat_schedule"]

def check_is_beat_schedule_param(obj:Union[Any, BeatScheduleParam]) -> bool:
    return all(
        key in obj for key in {"task", "schedule"}
    )
    
def check_is_beat_schedule(obj: Union[dict[str, Any], BeatSchedule]) -> bool: 
    for value in obj.values():
        if check_is_beat_schedule_param(value) is False:
            return False
        
    return True