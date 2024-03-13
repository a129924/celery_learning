from typing import Optional, TypeVar

VT = TypeVar("VT")

__all__ = ["get_value_from_dotkey"]

def get_value_from_dotkey(obj: dict[str, VT], dotkey:str, sep: str = ".") -> VT:
    from functools import reduce

    keys = dotkey.split(sep=sep)

    return reduce(lambda prev, key: getattr(prev, key), keys[:1], getattr(obj, keys[0]))

