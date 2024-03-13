from typing import TypeVar, Mapping

VT = TypeVar("VT")

__all__ = ["get_value_from_dotkey"]


def get_value_from_dotkey(obj: Mapping[str, VT], dotkey: str, sep: str = ".") -> VT:
    """_summary_

    Args:
        obj (dict[str, dict[str, VT]]): _description_
        dotkey (str): _description_
        sep (str, optional): _description_. Defaults to ".".

    Returns:
        dict[str, VT]: _description_

    ## Example Code
    ```python=
    >>> config_obj = {
        'config' : {
            'task_name' : BeatScheduleParam,
            ...
        }
    }

    >>> config = get_value_from_dotkey(config_obj, config)
    ```
    """
    from functools import reduce

    keys = dotkey.split(sep=sep)

    return reduce(lambda prev, key: getattr(prev, key), keys[:1], getattr(obj, keys[0]))
