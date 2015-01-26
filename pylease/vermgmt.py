from distutils.version import StrictVersion
import re
import string

__author__ = 'bagrat'


class DevedVersion(StrictVersion):
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
        self._increase_version(count, 0)

    def increase_minor(self, count=1):
        self._increase_version(count, 1)

    def increase_patch(self, count=1):
        self._increase_version(count, 2)

    def increase_dev(self, level=1):
        self.dev += level

    def __str__(self):
        prefix = StrictVersion.__str__(self)
        suffix = '.dev{ver}'.format(ver=self.dev) if self.dev > 0 else ''

        return '{prefix}{suffix}'.format(prefix=prefix, suffix=suffix)
