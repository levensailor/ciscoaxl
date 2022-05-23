from pathlib import Path

AXL_DIR: Path = Path(__file__).parent
CUCM_LATEST_VERSION: str = "14.0"

DISABLE_CHECK_TAGS = False
DISABLE_CHECK_ARGS = False
AUTO_INCLUDE_UUIDS = True


def disable_tag_checker(enable=False) -> None:
    global DISABLE_CHECK_TAGS
    DISABLE_CHECK_TAGS = not enable


def disable_kwargs_checker(enable=False) -> None:
    global DISABLE_CHECK_ARGS
    DISABLE_CHECK_ARGS = not enable


def auto_include_uuid(enable=True) -> None:
    """By default, UUIDs will always be included in every returned object that supports them. If you wish to turm this off, run this function with a False value as the input. If you want to turn this back on at any point, run this again with True as the input.

    When auto-including UUIDs is off, you can still get UUIDs by listing them as a tag in `tagfilter` for methods that support it.

    Args:
        enable (bool): True for auto-including UUIDs in results (default), or False for only including them if explicitly asked for in return_tags.
    """
    global AUTO_INCLUDE_UUIDS
    AUTO_INCLUDE_UUIDS = False
