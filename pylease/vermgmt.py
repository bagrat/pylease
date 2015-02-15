from distutils.version import StrictVersion
import re
import string

__author__ = 'bagrat'


class DevedVersion(StrictVersion):
    """
    An extension to StrictVersion, which includes a dev component.
    """
    _strict_re_str = StrictVersion.version_re.pattern[1:-1]
    _deved_re_str = r'^({strict_re}) (\.dev(\d+))?$'\
        .format(strict_re=_strict_re_str)
    _deved_re = re.compile(_deved_re_str, re.VERBOSE)

    def __init__(self, vstring=None):
        match = self._deved_re.match(vstring)

        if not match:
            raise ValueError("Invalid version number '%s'" % vstring)
        else:
            dev_num_index = len(match.groups())
            if match.group(dev_num_index):
                self.dev = string.atoi(match.group(dev_num_index))
            else:
                self.dev = 0
            vstring = match.group(1)

        StrictVersion.__init__(self, vstring)

    def _increase_version(self, count=1, index=0):
        """
        Increase the index'th level of the version by count
        """
        old_version = self.version

        old_comp = old_version[index]
        new_comp = old_comp + count

        new_version = []

        for i, comp in enumerate(old_version):
            if i == index:
                new_version.append(new_comp)
            elif i > index:
                new_version.append(0)
            else:
                new_version.append(old_version[i])

        self.dev = 0
        self.version = tuple(new_version)

    def increase_major(self, count=1):
        """
        Increase the major version by count
        """
        self._increase_version(count, 0)

    def increase_minor(self, count=1):
        """
        Increase the minor version by count
        """
        self._increase_version(count, 1)

    def increase_patch(self, count=1):
        """
        Increase the patch version by count
        """
        self._increase_version(count, 2)

    def increase_dev(self, level=1):
        """
        Increase the dev version by count
        """
        self.dev += level

    def __str__(self):
        prefix = StrictVersion.__str__(self)
        suffix = '.dev{ver}'.format(ver=self.dev) if self.dev > 0 else ''

        return '{prefix}{suffix}'.format(prefix=prefix, suffix=suffix)


class VersionContainer(object):  # pragma: no cover
    def __init__(self):
        super(VersionContainer, self).__init__()

        self.version = None

    def set_version(self, version):
        self.version = version
