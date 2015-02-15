from pylease.ex import ReleaseError
from pylease.vermgmt import DevedVersion

__author__ = 'bagrat'

_levels = ['major', 'minor', 'patch', 'dev']
_default_level_index = 0
default_level = _levels[_default_level_index]


def release(old, level=default_level, count=1):
    """
    Returns a new version which is ``count`` times higher from ``old`` by level ``level``.

    :param old: The current version
    :param level: The level to be released to, i.e. one of the following - major, minor, patch, dev
    :param count: The number to increase the level by
    """

    if level not in _levels:
        raise ReleaseError('Unknown release level: {level}\nShould be one of those: {levels}'.format(level=level, levels=_levels))

    new_version = DevedVersion(old)

    if level == 'major':
        new_version.increase_major(count)
    elif level == 'minor':
        new_version.increase_minor(count)
    elif level == 'patch':
        new_version.increase_patch(count)
    elif level == 'dev':
        new_version.increase_dev(count)

    return new_version
