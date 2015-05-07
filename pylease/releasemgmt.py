from pylease.ex import ReleaseError
from pylease.vermgmt import DevedVersion

__author__ = 'bagrat'

_LEVELS = ['major', 'minor', 'patch', 'dev']
_DEFAULT_LEVEL_INDEX = 0
DEFAULT_LEVEL = _LEVELS[_DEFAULT_LEVEL_INDEX]


def release(old, level=DEFAULT_LEVEL, count=1):
    """
    Returns a new version which is ``count`` times higher from ``old`` by level ``level``.

    :param old: The current version
    :param level: The level to be released to, i.e. one of the following - major, minor, patch, dev
    :param count: The number to increase the level by
    """

    if level not in _LEVELS:
        raise ReleaseError('Unknown release level: {level}\nShould be one of those: {levels}'.format(level=level, levels=_LEVELS))

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
