from functools import wraps
from typing import Callable, TypeVar, Union, Sequence
import inspect
from zeep.helpers import serialize_object
from copy import deepcopy
from ciscoaxl.exceptions import DumbProgrammerException
from ciscoaxl.wsdl import (
    get_return_tags,
    fix_return_tags,
    validate_arguments,
)
import ciscoaxl.configs as cfg
import asyncio

class _StaticIdentity:
    def __init__(self, value: str) -> None:
        self.__value__ = value

    def __repr__(self) -> str:
        return self.__value__

Empty = _StaticIdentity("Empty")

TCallable = TypeVar("TCallable", bound=Callable)


def _tag_serialize_filter(tags: Union[list, dict], data: dict) -> dict:
    """Filters out data that is not wanted by `tags` and cleans up annoyances like '_value_1' keys

    :param tags: Tags wanted in the result data
    :param data: AXL data in serialized form
    :return: Cleaned data with unwanted tags removed
    """

    def check_value(d: dict) -> dict:
        d_copy = d.copy()
        for tag, value in d_copy.items():
            if type(value) == dict:
                if "_value_1" in value:
                    d_copy[tag] = value["_value_1"]
                else:
                    d_copy[tag] = check_value(value)
            elif type(value) == list:
                for i, d in enumerate(deepcopy(value)):
                    if type(d) == dict:
                        value[i] = check_value(d)
        return d_copy

    # ctiid may not have use, remove if there
    # ? not entirely sure about this, will find out later
    data.pop("ctiid", None)

    if tags is None:
        checked_data = check_value(data)
        if not cfg.AUTO_INCLUDE_UUIDS:
            checked_data.pop("uuid", None)
        return checked_data

    working_data = deepcopy(data)
    for tag, value in data.items():
        if tag == "uuid":
            # * UUIDs are not included in wsdl descriptors, so they won't
            # * show up automatically in 'tags'. We will always keep them in
            # * unless AUTO_INCLUDE_UUIDS has been turned off. Then, we will
            # * only keep UUIDs if 'uuid' is specified in return_tags
            if cfg.AUTO_INCLUDE_UUIDS:
                continue
            elif "uuid" not in tags:
                working_data.pop("uuid", None)
        elif tag not in tags and len(tags) > 0:
            working_data.pop(tag, None)
        elif type(value) == dict:
            if "_value_1" in value:
                working_data[tag] = value["_value_1"]
            else:
                working_data[tag] = check_value(value)
        elif type(value) == list:
            for i, d in enumerate(deepcopy(value)):
                if type(d) == dict:
                    value[i] = check_value(d)
    return working_data


"""Decorator that will process the func's `return_tags` parameter
and perform the following actions:

- Check to see that all provided tags are valid 'returnedTags' base values
- Convert `return_tags`' list of base tag elements into a nested dict of all needed child tags

The `element_name` should be the name of the element being called by the func.
"""


def check_tags(element_name: str, children: Union[str, Sequence[str], None] = None):
    def check_tags_decorator(func: TCallable) -> TCallable:
        def processing(func, args, kwargs, children):
            if (
                tags_param := inspect.signature(func).parameters.get(
                    "return_tags", Empty
                )
            ) is Empty:
                raise DumbProgrammerException(
                    f"No 'return_tags' param on {func.__name__}()"
                )
            if tags_param.kind != tags_param.KEYWORD_ONLY:
                raise DumbProgrammerException(
                    f"Forgot to add '*' before return_tags on {func.__name__}()"
                )
            if not element_name:
                raise DumbProgrammerException(
                    f"Forgot to provide element_name in check_tags decorator on {func.__name__}!!!"
                )
            if children is not None:
                if not isinstance(children, Sequence):
                    raise DumbProgrammerException(
                        "'children' should be either a str or Sequence[str] if not None"
                    )
                if type(children) == str:
                    children = [children]

            if "return_tags" not in kwargs:
                # tags are default
                # if len(tags_param.default) == 0:
                if tags_param.default is None:
                    kwargs["return_tags"] = fix_return_tags(
                        z_client=args[0].zeep,
                        element_name=element_name,
                        tags=get_return_tags(args[0].zeep, element_name),
                        children=children,
                    )
            elif type(kwargs["return_tags"]) == list:
                # supply all legal tags if an empty list is provided
                if len(kwargs["return_tags"]) == 0:
                    kwargs["return_tags"] = fix_return_tags(
                        z_client=args[0].zeep,
                        element_name=element_name,
                        tags=get_return_tags(args[0].zeep, element_name),
                        children=children,
                    )
                else:
                    kwargs["return_tags"] = fix_return_tags(
                        z_client=args[0].zeep,
                        element_name=element_name,
                        tags=kwargs["return_tags"],
                        children=children,
                    )

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # if cfg.DISABLE_CHECK_ARGS:
            #     return await func(*args, **kwargs)
            processing(func, args, kwargs, children)
            return await func(*args, **kwargs)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # if cfg.DISABLE_CHECK_TAGS:
            #     return func(*args, **kwargs)
            processing(func, args, kwargs, children)
            return func(*args, **kwargs)

        if inspect.iscoroutinefunction(func):
            async_wrapper.element_name = element_name
            async_wrapper.check = "tags"
            return async_wrapper
        else:
            wrapper.element_name = element_name
            wrapper.check = "tags"
            return wrapper

    return check_tags_decorator