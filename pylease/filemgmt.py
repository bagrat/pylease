import inspect
import re

from pylease import vspec
from pylease.ex import VersionSpecError

__author__ = 'bagrat'


def _find_version_class_name():
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
        raise VersionSpecError('The version specification module MUST define exactly one class.')

    return result


_version_name = _find_version_class_name()
_version_regexp = "(?P<start>{version_name}\([\'\"])[0-9a-zA-Z\.]*(?P<end>[\'\"]\))".format(version_name=_version_name)


def replace_version(setup_py, to):
    re_obj = re.compile(_version_regexp)
    matches = re_obj.findall(setup_py)
    replacement = "\g<start>{to}\g<end>".format(to=to)

    if not len(matches) == 1:
        raise VersionSpecError('More than one version specification found.')

    return re_obj.sub(replacement, setup_py)

