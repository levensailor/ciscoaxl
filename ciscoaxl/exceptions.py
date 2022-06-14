from typing import Sequence, List
import json


class WSDLException(Exception):
    pass


class WSDLInvalidArgument(Exception):
    def __init__(self, argument: str, element_name: str, *args: object) -> None:
        self.arg = argument
        self.element = element_name
        super().__init__(*args)

    def __str__(self) -> str:
        return f"'{self.arg}' is not a valid argument for {self.element}"


class WSDLMissingArguments(Exception):
    def __init__(self, arguments: Sequence, element_name: str, *args: object) -> None:
        self.arguments = arguments
        self.element = element_name
        super().__init__(*args)

    def __str__(self) -> str:
        return f"The following arguments are missing from {self.element}: {', '.join(self.arguments)}"


def _list_options(options: Sequence) -> str:
    o_strings: list[str] = []
    for i, option in enumerate(options):
        if type(option) == str:
            o_strings.append(f"{i+1}) '{option}'")
        elif type(option) == list:
            o_strings.append(f"{i+1}) " + ", ".join([f"'{o}'" for o in option]))
    return "\n".join(o_strings)


class WSDLChoiceException(WSDLMissingArguments):
    def __init__(
        self,
        arguments: Sequence,
        element_name: str,
        return_tags: bool = False,
        *args: object,
    ) -> None:
        self.return_tags = return_tags
        super().__init__(arguments, element_name, *args)

    def __str__(self) -> str:
        return (
            f"For {self.element}, you can choose only ONE of the following"
            + f"{' for the returned tags' if self.return_tags else ''}:"
            + "\n"
            + f"{_list_options(self.arguments)}"
        )


class WSDLDrillDownException(WSDLInvalidArgument):
    def __init__(
        self, argument: str, structure: dict, element_name: str, *args: object
    ) -> None:
        try:
            self.structure = json.dumps(structure, indent=2)
        except TypeError:
            self.structure = str(structure)

        super().__init__(argument, element_name, *args)

    def __str__(self) -> str:
        return f"'{self.arg}' in {self.element} must be a dict of the following format:\n\n{self.structure}"


class WSDLValueOnlyException(WSDLInvalidArgument):
    def __str__(self) -> str:
        return f"'{self.arg}' in {self.element} should only be a single value."


class TagNotValid(Exception):
    def __init__(
        self, tag: str, valid_tags: List[str], *args, func=None, elem_name=""
    ) -> None:
        self.tag = tag
        self.func = func
        self.element = elem_name
        self.valid_tags = valid_tags
        super().__init__(*args)

    def __str__(self) -> str:
        if self.func is not None:
            return f"'{self.tag}; is not a valid return tag for {self.func.__name__}(). Valid tags are:\n{self.valid_tags}"
        elif self.element:
            return f"'{self.tag}; is not a valid return tag for {self.element}. Valid tags are:\n{self.valid_tags}"
        else:
            return f"Invalid tag encountered: '{self.tag}'"


class InvalidArguments(Exception):
    pass
