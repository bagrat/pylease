from pylease.ex import ReleaseError
from pylease.filemgmt import update_file
from pylease.vermgmt import DevedVersion

__author__ = 'bagrat'

_levels = ['major', 'minor', 'patch', 'dev']
_default_level_index = 0
default_level = _levels[_default_level_index]


def release(current, level=default_level, count=1):
    current_version = DevedVersion(current)

    if level not in _levels:
        raise ReleaseError(
            'Unknown release level: {level}\nShould be one of those: {levels}'
            .format(level=level, levels=_levels))

    if level == 'major':
        current_version.increase_major(count)
    elif level == 'minor':
        current_version.increase_minor(count)
    elif level == 'patch':
        current_version.increase_patch(count)
    elif level == 'dev':
        current_version.increase_dev(count)

    update_file(str(current_version))


def rollback(previous_version):  # pragma: no cover
    update_file(str(previous_version))
