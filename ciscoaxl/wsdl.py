from typing import Any, Dict, List, Union
from zeep import Client
from zeep.exceptions import LookupError
from zeep.xsd.elements.element import Element
from zeep.xsd.elements.indicators import Choice, Sequence
from zeep.xsd import Nil, AnyObject
from ciscoaxl.exceptions import (
    WSDLDrillDownException,
    WSDLException,
    WSDLInvalidArgument,
    WSDLChoiceException,
    TagNotValid,
    WSDLValueOnlyException,
)
from termcolor import colored


class AXLElement:
    """An object with a tree-like structure useful for navigating and getting data from XSD elements"""

    def __init__(self, element: Union[Element, Choice], parent=None) -> None:
        """An object with a tree-like structure useful for navigating and getting data from XSD elements

        :param element: An XSD (Zeep) element
        :param parent: DO NOT USE, for internal recursion only, defaults to None
        """
        self.elem = element
        self.parent = parent

        if type(element) == Sequence:
            self.name = "[ group ]"
            self.type = Sequence
            self.children = [AXLElement(e[1], parent=self) for e in element.elements]
            if self.parent is not None and self.parent.type == Choice:
                self.needed = False
            else:
                self.needed = not element.is_optional
        elif type(element) == Choice:
            self.name = "[ choice ]"
            self.type = Choice
            self.children = [
                AXLElement(e[1], parent=self) for e in element.elements_nested
            ]
            self.child_names = [e.name for e in self.children]
            self.needed = bool(self.elem.min_occurs != 0)
        elif type(element) == Element:
            self.name = element.name
            self.type = element.type
            if self.parent is not None and self.parent.type == Choice:
                self.needed = False
            else:
                self.needed = not element.is_optional
            if hasattr(element.type, "elements"):
                package = element.type.elements_nested[0][1]
                if type(package) == Sequence:
                    self.children = [
                        AXLElement(e, self)
                        for e in package
                        if getattr(e, "name", None) not in ("_value_1", None)
                        or type(e) == Choice
                    ]
                elif type(package) == Element:
                    self.children = (
                        [AXLElement(package, self)]
                        if not package.name.startswith("_value_")
                        else []
                    )
                elif type(package) == Choice:
                    self.children = [AXLElement(package, self)]
                else:
                    raise WSDLException(f"Unknown package format '{type(package)}'")
            else:
                self.children = []
        else:
            raise WSDLException(f"Unknown element format '{type(element)}'")

    def __getitem__(self, key):
        value = self.get(key, None)
        if value is not None:
            return value
        else:
            raise KeyError(key)

    def __repr__(self) -> str:
        name = self.name
        xsd_type = type(self.type).__name__
        children = len(self.children)
        return f"AXLElement(name={name}, xsd_type={xsd_type}, children={children})"

    def _parent_chain(self) -> str:
        """Returns a formatted string showing the path of nodes along the tree that leads to this element.
        If this node has no parent, returns only the name of the node itself.

        :return: A formatted string of parent elements
        """
        if self.parent is None:
            return self.name
        elif self.type == Choice or self.type == Sequence:
            return self.parent._parent_chain()
        else:
            return self.parent._parent_chain() + "." + self.name

    def _parent_chain_required(self) -> bool:
        """Determines if this node is required when its parent node has been implemented

        :return: True if required by parent, False if not required
        """
        if self.parent is None and self.needed:
            return True
        elif self.needed:
            return self.parent._parent_chain_required()
        else:
            return False

    def children_dict(self) -> dict:
        """Returns a dictionary of all children nodes from this node

        :return: A dictionary of children where a bottom child is given '' as its value
        """
        c_dict = dict()
        for child in self.children:
            if child.type == Choice or child.type == Sequence:
                i = 1
                base_name = child.name.split(" ")[1]
                while f"[ {base_name}{i} ]" in c_dict:
                    i += 1
                c_dict[f"[ {base_name}{i} ]"] = child.children_dict()
            elif child.children:
                c_dict[child.name] = child.children_dict()
            else:
                c_dict[child.name] = ""
        return c_dict

    def children_names(self) -> list:
        """Returns a list of strings of all 1st generation children from this node

        :return: A list of strings representing this node's children
        """
        child_strings = []
        for child in self.children:
            if child.type == Choice or child.type == Sequence:
                if child.type == Choice:
                    sep = ("(", " | ", ")")
                else:
                    sep = ("[", " + ", "]")
                child_strings.append(
                    sep[0] + sep[1].join([c.name for c in child.children]) + sep[2]
                )
            else:
                child_strings.append(child.name)
        return child_strings

    def print_tree(self, indent=0, show_types=False, show_required=True) -> None:
        """Print a color-coded representation of the tree, starting from this node

        :param indent: DO NOT USE, for recursive purposes only, defaults to 0
        :param show_types: Shows the types of all elements next to their names, defaults to False
        :param show_required: Shows if an element is required, or only required if its parent is used, defaults to True
        """
        branch_str = f"{'  ' * indent if indent < 2 else ('  |' * (indent - 1)) + '  '}{'┗ ' if indent else ''}"
        name_str = self.name
        atrib_str = ""

        if self.type == Choice:
            name_str = colored(self.name, "green")
            atrib_str += (
                "(choose only one " + colored("child", "magenta", attrs=["bold"]) + ")"
            )

        if show_required and self.needed and self.parent is not None:
            if self._parent_chain_required():
                if self.type not in (Sequence, Choice):
                    name_str = colored(self.name, "cyan")
                atrib_str += colored(" (required)", "blue")
            else:
                atrib_str += colored(" (required if parent is used)", "yellow")
        elif self.parent is not None and self.parent.type == Choice:
            name_str = colored(self.name, "magenta")
            # atrib_str += colored(" (must choose only one)", "magenta")

        if (
            show_types
            and self.type not in (Sequence, Choice)
            and self.parent is not None
        ):
            atrib_str += colored(f" ({type(self.type).__name__})", "green")

        print(branch_str, name_str, atrib_str, sep="")

        for child in self.children:
            child.print_tree(indent + 1, show_types, show_required)

    def get(self, name: str, default=None) -> Union["AXLElement", None]:
        """Wrapper for dict-like get method"""
        if not name:
            return default
        for child in self.children:
            if getattr(child, "name", None) == name:
                return child
            elif child.type == Choice or child.type == Sequence:
                finding = child.get(name)
                if finding is not None:
                    return finding
        else:
            return default

    def find(self, name: str) -> Union["AXLElement", None]:
        """Similar to get(), but does a depth search to find the first node in the tree with a matching name

        :param name: The name of the node to be searched for
        :return: A node matching the given name, if found, or None if not found
        """
        if not name:
            return None

        for child in self.children:
            if getattr(child, "name", None) == name:
                return child
            elif child.children:
                result = child.find(name)
                if result is not None:
                    return result
        else:
            return None

    def validate(self, *args, **kwargs) -> None:
        """Validates that the given args and kwargs would be valid in constructing the element at this node.
        Raises an exception if a given arg/kwarg is not valid, with details on what the issue is.
        """

        def choice_peek(choice: AXLElement) -> list:
            peek_names: list[str] = []
            for child in choice.children:
                if not child.name.startswith("[ group"):
                    peek_names.append(child.name)
                elif child.type == Sequence:
                    peek_names.extend([c.name for c in child.children])
            return peek_names

        if args:
            raise WSDLException(
                f"A non-named argument was supplied for {self.name} with the value {args[0]}. "
                + "Arguments for AXL API requests must all be named (kwargs)."
            )

        c_dict = self.children_dict(required=True)
        if self.type == Choice:
            groups: list[list[str]] = [
                [e.name for e in c.children]
                for c in self.children
                if c.name == "[ group ]"
            ]
            elements: list[str] = [
                c.name for c in self.children if not c.name.startswith("[ ")
            ]
            g_found = [g for g in groups if any(e in kwargs for e in g)]
            e_found = [e for e in elements if e in kwargs]
            if len(g_found) + len(e_found) != 1:
                raise WSDLChoiceException(
                    arguments=elements + groups,
                    element_name=self.parent._parent_chain(),
                )
        else:
            for name, value in kwargs.items():
                if type(value) not in (dict, list):  # * normal tag-value pairs
                    if name not in c_dict:
                        choice_list = [
                            c for c in self.children if c.name == "[ choice ]"
                        ]
                        if not choice_list:
                            raise WSDLInvalidArgument(name, self._parent_chain())
                        for choice in choice_list:
                            if name in choice_peek(choice):
                                choice.validate(**kwargs)
                                break
                        else:
                            raise WSDLInvalidArgument(name, self._parent_chain())
                    elif type(c_dict[name]) == dict:
                        raise WSDLDrillDownException(
                            name, c_dict[name], self._parent_chain()
                        )
                elif type(value) == dict:  # * complex types
                    if name not in c_dict:
                        choice_list = [
                            c for c in self.children if c.name == "[ choice ]"
                        ]
                        if not choice_list:
                            raise WSDLInvalidArgument(name, self._parent_chain())
                        for choice in choice_list:
                            if name in choice.children_dict():
                                [c for c in choice.children if c.name == name][
                                    0
                                ].validate(**value)
                                break
                        else:
                            raise WSDLInvalidArgument(name, self._parent_chain())
                    elif type(c_dict[name]) != dict:
                        raise WSDLValueOnlyException(name, self._parent_chain())
                    else:
                        [c for c in self.children if c.name == name][0].validate(
                            **value
                        )
                elif type(value) == list:  # * list of elements
                    if not value or type(value) == str:
                        self.validate(**{name: ""})
                    elif type(value[0]) == dict:
                        for entry in value:
                            self.validate(**{name: entry})

    def return_tags(self) -> dict:
        """Finds the 'returnedTags' element of the tree and returns a dictionary containing the layout of the accepted tags.

        :return: A nested dictionary of tags
        """
        if self.parent is not None:
            return self.parent.return_tags()

        tags_element = self.get("returnedTags")
        if tags_element is None:
            return {}

        def nil_to_str(d: dict) -> dict:
            for name, value in d.items():
                if type(value) == dict:
                    nil_to_str(value)
                elif value in (Nil, True):
                    d[name] = ""

        tags_dict = tags_element.to_dict()["returnedTags"]
        for value in tags_dict.values():
            if type(value) == dict:
                nil_to_str(value)

        return tags_dict

    def to_dict(self) -> dict:
        """Returns a dictionary of the tree with default values suppled where applicable.

        :return: A nested dictionary of children including this node as the parent.
        """
        if not self.children:
            if hasattr(self.type, "elements"):
                return {self.name: AnyObject(self.type, {})}
            else:
                return {self.name: self.type.pythonvalue(True)}
        elif self.type == Choice:
            return self.children[0].to_dict()
        elif self.type == Sequence:
            seq_dict: dict = dict()
            for child in self.children:
                seq_dict.update(child.to_dict())
            return seq_dict
        else:
            children_dict: dict = dict()
            for child in self.children:
                children_dict.update(child.to_dict())
            return {self.name: children_dict}

    def needed_only(self) -> Union["AXLElement", None]:
        """Creates a new AXLElement tree with ONLY the required nodes.

        :return: A copy of this AXLElement tree with non-needed nodes removed.
        """
        if self.parent is None:
            needed_root = AXLElement(self.elem)
            needed_root.children[:] = [c for c in needed_root.children if c.needed]
            for child in needed_root.children:
                child.needed_only()
            return needed_root
        elif self.type == Choice:
            for child in self.children:
                child.needed_only()
        else:
            self.children[:] = [c for c in self.children if c.needed]
            for child in self.children:
                child.needed_only()

    def first_choice(self, *, root=True) -> "AXLElement":
        """Given that this node is a Choice node, returns the first node that isn't a Choice or Sequence node.

        :param root: DO NOT USE, recursive use only, defaults to True
        :return: A child AXLElement node that is not a Choice or Sequence node
        """
        if root and self.type != Choice:
            raise WSDLException(
                f"Can't use first choice on non-choice node '{self.name}'"
            )

        if self.children[0].type not in (Choice, Sequence):
            return self.children[0]
        elif self.children[0].type == Choice:
            return self.children[0].first_choice(root=False)
        elif self.children[0].type == Sequence:
            # try to do ANYTHING but return a sequence
            if len(self.children) == 1:
                return self.children[0]
            for child in self.children[1:]:
                if child.type == Choice:
                    return child.first_choice(root=False)
                elif child.type != Sequence:
                    return child
            else:
                return self.children[0]


def __get_element_by_name(z_client: Client, element_name: str) -> Element:
    """Pulls the XSD element from the active Zeep client

    :param z_client: The active Zeep client object that has parsed the WSDL schema
    :param element_name: The name of the element needed
    :return: A Zeep XSD element
    """
    try:
        element = z_client.get_element(f"ns0:{element_name}")
    except LookupError:
        raise WSDLException(f"Could not find element {element_name}") from None
    return element


def get_return_tags(z_client: Client, element_name: str) -> list:
    """Returns a list of the top-most tags in an element's returnedTags node

    :param z_client: The active Zeep client object that has parsed the WSDL schema
    :param element_name: THe name of the element needed
    :return: A list of top-level return tags
    """
    try:
        return_tree = get_tree(z_client, element_name)["returnedTags"]
    except KeyError:
        raise WSDLException(
            f"Element '{element_name}' has no returnedTags sub-element"
        ) from None

    def extract_return_tags(tree: AXLElement) -> list:
        tags = []
        for child in tree.children:
            if child.type == Choice:
                best = child.first_choice()
                if best.type == Sequence:
                    tags.extend(extract_return_tags(best))
                else:
                    tags.append(best.name)
            elif child.type == Sequence:
                for grandchild in child.children:
                    tags.extend(extract_return_tags(grandchild))
            else:
                tags.append(child.name)
        return tags

    return extract_return_tags(return_tree)


def get_tree(z_client: Client, element_name: str) -> AXLElement:
    """Creates an AXLElement object emulating the XSD element with the given element name.

    :param z_client: The active Zeep client object that has parsed the WSDL schema
    :param element_name: The name of the element needed
    :return: An AXLElement object
    """
    return AXLElement(__get_element_by_name(z_client, element_name))


def fix_return_tags(
    z_client: Client,
    element_name: str,
    tags: Union[List[str], Dict[str, Any], None],
    children: Union[List[str], None] = None,
) -> dict:
    """Takes the given list of tags (or dict, only uses top-level keys) and filters out all of the given element's
     returnedTags children that are not included in the given tags.

    :param z_client: The active Zeep client object that has parsed the WSDL schema
    :param element_name: The name of the element needed
    :param tags: A list or dict of the wanted tags
    :param children: If you only need the return tags of a specific child (e.g. you're returning "Line" from getPhone),
    you can supply the chain of children from the root node down to what you need, defaults to None
    :return: A dict of tags (with default values) for use in returnedTags
    """
    if not tags:  # empty list/dict or None
        tags = get_return_tags(z_client, element_name)

    tree = get_tree(z_client, element_name)

    if tree.get("returnedTags", None) is None:
        raise WSDLException(f"Element '{element_name}' has no returnedTags sub-element")

    tag_tree = tree["returnedTags"]
    tag_stack = {}
    return_tags = tag_stack

    if children is not None:
        for i, child in enumerate(children):
            tag_tree = tag_tree.get(child, None)

            if tag_tree is None:
                raise WSDLException(
                    f"{element_name} does not have child of {'->'.join(children[:i])}"
                )

            # add child to stack, position return_tags at
            # bottom of stack
            return_tags[child] = {}
            return_tags = return_tags[child]

    # fill return_tags with nested tags found in tree
    for tag in tags:
        # uuid is always included in AXK return, but confuses returnTags, skip it
        if tag == "uuid":
            continue

        found_node = tag_tree.get(tag, None)
        if found_node is not None:
            if found_node.children:
                return_tags.update(found_node.to_dict())
            else:
                return_tags[
                    tag
                ] = Nil  # Nil works best for tree leaves (for some reason)
        # check inside "choice" nodes to find the tag
        elif [c for c in tag_tree.children if c.type == Choice]:
            choice_nodes = [c for c in tag_tree.children if c.type == Choice]
            for choice in choice_nodes:
                found_node = choice.get(tag, None)
                if found_node is not None:
                    other_choices = [
                        c.name for c in found_node.children if c.name != tag
                    ]
                    if any([(c in tags) for c in other_choices]):
                        raise WSDLChoiceException(
                            other_choices + [tag], element_name, return_tags=True
                        )
                    else:
                        if found_node.children:
                            return_tags.update(found_node.to_dict())
                        else:
                            return_tags[tag] = Nil
                    break
            else:
                raise TagNotValid(
                    tag, tag_tree.children_names(), elem_name=element_name
                )
        else:
            raise TagNotValid(tag, tag_tree.children_names(), elem_name=element_name)

    return tag_stack


def print_element_layout(
    z_client: Client, element_name: str, show_required=True, show_types=False
) -> None:
    """Prints a color-coded tree of an element

    :param z_client: The active Zeep client object that has parsed the WSDL schema
    :param element_name: The name of the element needed
    :param show_required: Prints information on if a node is required, defaults to True
    :param show_types: Prints element types next to the element names, defaults to False
    """
    root: AXLElement = AXLElement(__get_element_by_name(z_client, element_name))
    root.print_tree(show_required=show_required, show_types=show_types)


def print_required_element_layout(
    z_client: Client, element_name: str, show_types=False
) -> None:
    """Prints a color-coded tree of ONLY the required nodes of an element

    :param z_client: The active Zeep client object that has parsed the WSDL schema
    :param element_name: The name of the element needed
    :param show_types: Prints element types next to the element names, defaults to False
    """
    root: AXLElement = AXLElement(__get_element_by_name(z_client, element_name))
    root.needed_only().print_tree(show_types=show_types, show_required=True)


def print_return_tags_layout(
    z_client: Client, element_name: str, show_required=False, show_types=False
) -> None:
    """Prints a color-coded tree of the returnedTags nodes in a given element

    :param z_client: The active Zeep client object that has parsed the WSDL schema
    :param element_name: The name of the element needed
    :param show_required: Prints information on if a node is required, defaults to False
    :param show_types: Prints element types next to the element names, defaults to False
    """
    root: AXLElement = AXLElement(__get_element_by_name(z_client, element_name))
    r_tags = root.find("returnedTags")
    if r_tags is None:
        raise WSDLException(
            f"'returnedTags' element cannot be found within '{element_name}'"
        )
    else:
        r_tags.print_tree(show_types=show_types, show_required=show_required)


def validate_arguments(
    z_client: Client, element_name: str, child=None, **kwargs
) -> None:
    """Validates that the given kwargs would be valid in constructing the element at this node.
     Raises an exception if a given kwarg is not valid, with details on what the issue is.

    :param z_client: The active Zeep client object that has parsed the WSDL schema
    :param element_name: The name of the element needed
    :param child: A list of children leading down to the node to compare against, defaults to None
    """
    if not kwargs:
        return None

    root: AXLElement = get_tree(z_client, element_name)
    if (
        child is not None
    ):  # if the child needs to be the reference point instead of root node
        root = root.get(child)

    root.validate(**kwargs)
