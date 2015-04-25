__author__ = 'bagrat'


def replace_version(content, frm, to):
    """
    Replaces the value of the version specification value in the contents of
    ``setup_py`` from ``frm`` to ``to``.
    :param content: The string containing version specification
    :param to: The new version to be set
    :return: (result_content, number of occurrences)
    """
    frm_str = str(frm)
    to_str = str(to)

    count = content.count(frm_str)

    result_setup_py = content.replace(frm_str, to_str, count)

    return result_setup_py, count


def update_files(frm, to, files=None):
    """
    Update setup.py contents. See replace_version.
    :param to: The new version to be set.
    """
    counts = {}
    if not files:
        files = ['setup.py']
    for filename in files:
        with open(filename, 'r') as setup_py:
            content = setup_py.read()

            new_content, count = replace_version(content, frm, to)

            counts[filename] = count

        with open(filename, 'w') as setup_py:
            setup_py.write(new_content)

    return counts


class VersionRollback(object):
    def __init__(self, old_version, new_version, files=None):
        super(VersionRollback, self).__init__()

        self._old = old_version
        self._new = new_version
        self._files = files

    def rollback(self):
        update_files(self._new, self._old, self._files)
