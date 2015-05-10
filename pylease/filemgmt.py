__author__ = 'bagrat'


def replace_version(content, from_version, to_version):
    """
    Replaces the value of the version specification value in the contents of
    ``contents`` from ``from_version`` to ``to_version``.

    :param content: The string containing version specification
    :param to_version: The new version to be set
    :return: (result_content, number of occurrences)
    """
    frm_str = str(from_version)
    to_str = str(to_version)

    count = content.count(frm_str)

    result_setup_py = content.replace(frm_str, to_str, count)

    return result_setup_py, count


def update_files(from_version, to_version, files=None):
    """
    Update contents of files. See replace_version.

    :param from_version: The old version to be replaced.
    :param to_version: The new version to be set.
    :param files: A list of files, to update versions in.
    """
    counts = {}
    if not files:
        files = ['setup.py']
    for filename in files:
        with open(filename, 'r') as setup_py:
            content = setup_py.read()

            new_content, count = replace_version(content, from_version, to_version)

            counts[filename] = count

        with open(filename, 'w') as setup_py:
            setup_py.write(new_content)

    return counts


class VersionRollback(object):
    """
    A rollback object that simple rolls back the updated version.
    """
    def __init__(self, old_version, new_version, files=None):
        super(VersionRollback, self).__init__()

        self._old = old_version
        self._new = new_version
        self._files = files

    def rollback(self):
        update_files(self._new, self._old, self._files)
