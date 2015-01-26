import inspect
import re

from pylease import vspec
from pylease.ex import VersionSpecError

__author__ = 'bagrat'


def _find_version_class_name():
    """
    Finds the name of the version specification class. Done for easy
     renaming in future.
    :return: The name of the version specification class.
    """

    names = dir(vspec)

    result = None
    found_one = False
    for name in names:
        if inspect.isclass(vspec.__dict__[name]):
            if not found_one:
                result = name
                found_one = True
            else:
                result = None
                break

    if not result:
        raise VersionSpecError('The version specification module MUST define '
                               'exactly one class.')

    return result


_version_name = _find_version_class_name()
_version_regexp = "(?P<start>{version_name}\([\'\"])" \
                  "[0-9a-zA-Z\.]*" \
                  "(?P<end>[\'\"]\))".format(version_name=_version_name)


def replace_version(setup_py, to):
    """
    Replaces the value of the version specification value in the contents of
    setup_py to to.
    :param setup_py: The string containing version specification
    :param to: The new version to be set
    :return:
    """

    re_obj = re.compile(_version_regexp)
    matches = re_obj.findall(setup_py)
    replacement = "\g<start>{to}\g<end>".format(to=to)

    if not len(matches) == 1:
        raise VersionSpecError(
            'More than one or no any version specification found.')

    return re_obj.sub(replacement, setup_py)


def update_file(to):  # pragma: no cover
    """
    Update setup.py contents. See replace_version.
    :param to: The new version to be set.
    """

    filename = 'setup.py'

    with open(filename, 'r') as setup_py:
        content = setup_py.read()

        new_content = replace_version(content, to)

    with open(filename, 'w') as setup_py:
        setup_py.write(new_content)
