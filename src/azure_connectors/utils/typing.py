from typing import Any, NamedTuple, NewType


class SplitKwargs(NamedTuple):
    cls_kwargs: dict[str, Any]
    remaining_kwargs: dict[str, Any]


ParamMap = NewType("ParamMap", dict[str, str])
"""
A dictionary mapping an object's property names to keyword argument names.
"""
