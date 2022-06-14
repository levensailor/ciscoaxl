from functools import wraps, partial
from typing import Callable, OrderedDict, TypeVar, Union, Sequence
import inspect
from zeep.xsd.valueobjects import CompoundValue
from copy import deepcopy
from ciscoaxl.wsdl import fix_return_tags
import ciscoaxl.config as cfg


class _StaticIdentity:
    def __init__(self, value: str) -> None:
        self.__value__ = value

    def __repr__(self) -> str:
        return self.__value__


Missing = _StaticIdentity("Missing")

TCallable = TypeVar("TCallable", bound=Callable)


def _tag_serialize_filter(tags: Union[list, dict], data: dict) -> dict:
    """Filters out data that is not wanted by `tags` and cleans up annoyances like '_value_1' keys

    :param tags: Tags wanted in the result data
    :param data: AXL data in serialized form
    :return: Cleaned data with unwanted tags removed
    """

    def check_for_value_1(d: dict) -> dict:
        d_copy = d.copy()
        for tag, value in d_copy.items():
            if type(value) == dict:
                if "_value_1" in value:
                    d_copy[tag] = value["_value_1"]
                else:
                    d_copy[tag] = check_for_value_1(value)
            elif type(value) == list:
                for i, d in enumerate(deepcopy(value)):
                    if type(d) == dict:
                        value[i] = check_for_value_1(d)
                    elif hasattr(d, "__values__"):
                        d_odict = d.__values__
                        d_filtered = check_for_value_1(dict(d_odict))
                        d.__values__ = OrderedDict(d_filtered)
                        value[i] = d
            elif hasattr(value, "__values__"):
                if "_value_1" in value:
                    d_copy[tag] = value["_value_1"]
                else:
                    value_odict = value.__values__
                    value_filtered = check_for_value_1(dict(value_odict))
                    value.__values__ = OrderedDict(value_filtered)
                    d_copy[tag] = value
        return d_copy

    # ctiid may not have use, remove if there
    # ? not entirely sure about this, will find out later
    data.pop("ctiid", None)

    if tags is None:
        # no tag filtering, but clean up any '_value_1' issues
        if cfg.DISABLE_VALUE1_RESOLVER:
            return data
        else:
            return check_for_value_1(data)

    working_data = deepcopy(data)
    for tag, value in data.items():
        if tag == "uuid":
            # * UUIDs are not included in wsdl descriptors, so they won't
            # * show up automatically in 'tags'. We will always keep them in.
            continue
        elif tag not in tags and len(tags) > 0:
            working_data.pop(tag, None)
        elif cfg.DISABLE_VALUE1_RESOLVER:
            working_data[tag] = value
        elif type(value) == dict:
            if "_value_1" in value:
                working_data[tag] = value["_value_1"]
            else:
                working_data[tag] = check_for_value_1(value)
        elif hasattr(value, "__values__"):
            if "_value_1" in value:
                working_data[tag] = value["_value_1"]
            else:
                value_odict = value.__values__
                value_filtered = check_for_value_1(dict(value_odict))
                value.__values__ = OrderedDict(value_filtered)
                working_data[tag] = value
        elif type(value) == list:
            for i, d in enumerate(deepcopy(value)):
                if type(d) == dict:
                    value[i] = check_for_value_1(d)
    return working_data


def _tag_zeep_filter(tags: Union[list, dict], data: CompoundValue) -> CompoundValue:
    data_odict: OrderedDict = data.__values__

    """Since we are supporting >3.6, we can go back and forth
    between OrderedDict and dict. For the Zeep object however,
    we will always want to supply it with its original typing
    of OrderedDict.
    """
    filtered_data: dict = _tag_serialize_filter(tags, dict(data_odict))
    data.__values__ = OrderedDict(filtered_data)
    return data


"""@check_tagfilter(element_name, children [optional])
Decorator that will process the func's `tagfilter` parameter
and perform the following actions:

- Check to see that all provided tags are valid 'returnedTags' base values
- Convert `tagfilter`' list/dict of base tag elements into a nested dict of all necessary child tags
- Filter out all returned objects' attributes that are not tags included in 'tagfilter' (works on lists of objects too)

If a user supplies [], {}, or None (or anything else with a false bool value), ALL tags for the given
element will be supplied for 'tagfilter' instead.

The `element_name` should be the name of the XSD element being called by the func.
'children' should only be used in very specific situation where your 'returnedTags' needs to be
    a subset of another element's returnedTags node. In that case, 'children' should either be a
    string or a list/tuple of strings representing the children required to travel down to get to
    the desired node.
"""


def check_tagfilter(element_name: str, children: Union[Sequence, None] = None):
    def check_tagfilter_decorator(func: TCallable) -> TCallable:
        def processing(func, args, kwargs, children) -> Union[tuple, None]:
            parameters = inspect.signature(func).parameters
            tag_param = parameters.get("tagfilter", Missing)

            if tag_param is Missing:
                raise Exception(
                    f"@check_tagfilter cannot be used on {func.__name__}(), has no 'tagfilter' parameter"
                )

            if type(children) == str:
                children = [children]
            adjust_tags = partial(
                fix_return_tags,
                args[0]._zeep,
                element_name,
                children=children,
            )

            # user supplied tagfilters as kwarg
            if "tagfilter" in kwargs:
                full_tags = adjust_tags(kwargs["tagfilter"])
                kwargs["tagfilter"] = full_tags
            # user supplied tagfilters as arg
            elif (len(args) - 1) >= list(parameters).index("tagfilter"):
                tag_arg_index = list(parameters).index("tagfilter")
                full_tags = adjust_tags(args[tag_arg_index])
                # func args are represented as a tuple, must replace immutable var
                new_args = list(args)
                new_args[tag_arg_index] = full_tags
                args = tuple(new_args)
            # no user-supplied value, there must be a default, use it
            else:
                full_tags = adjust_tags(tag_param.default)
                kwargs["tagfilter"] = full_tags

            return_value = func(*args, **kwargs)

            # leave only requested tags in the return
            if isinstance(return_value, CompoundValue):
                return _tag_zeep_filter(full_tags, return_value)
            elif type(return_value) == list:
                if len(return_value) == 0:
                    return []
                elif isinstance(return_value[0], CompoundValue):
                    return [_tag_zeep_filter(full_tags, e) for e in return_value]
            else:
                return return_value

        @wraps(func)
        def wrapper(*args, **kwargs):
            return processing(func, args, kwargs, children)

        return wrapper

    return check_tagfilter_decorator
