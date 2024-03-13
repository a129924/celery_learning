from typing import Union, Any

__all__ = ["JSON",]

JSON = Union[
    dict[str, Any],
    list[dict[str, Any]]
]