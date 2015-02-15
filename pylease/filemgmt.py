__author__ = 'bagrat'


def replace_version(setup_py, frm, to):
    """
    Replaces the value of the version specification value in the contents of
    ``setup_py`` from ``frm`` to ``to``.
    :param setup_py: The string containing version specification
    :param to: The new version to be set
    :return: (result_content, count of occurrences)
    """
    frm_str = str(frm)
    to_str = str(to)

    count = setup_py.count(frm_str)

    result_setup_py = setup_py.replace(frm_str, to_str, count)

    return result_setup_py, count


def update_setup_py(frm, to):  # pragma: no cover
    """
    Update setup.py contents. See replace_version.
    :param to: The new version to be set.
    """
    filename = 'setup.py'

    with open(filename, 'r') as setup_py:
        content = setup_py.read()

        new_content, count = replace_version(content, frm, to)

    with open(filename, 'w') as setup_py:
        setup_py.write(new_content)

    return count


class VersionRollback(object):  # pragma: no cover
    def __init__(self, old_version, new_version):
        super(VersionRollback, self).__init__()

        self.old = old_version
        self.new = new_version

    def rollback(self):
        update_setup_py(self.new, self.old)
