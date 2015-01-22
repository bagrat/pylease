from distutils.version import StrictVersion
import re
import string

__author__ = 'bagrat'


class DevedVersion(StrictVersion):
    _strict_re_str = StrictVersion.version_re.pattern[1:-1]
    _deved_re_str = r'^({strict_re}) (dev(\d+))?$'.format(strict_re=_strict_re_str)
    _deved_re = re.compile(_deved_re_str, re.VERBOSE)

    def __init__(self, vstring=None):
        match = self._deved_re.match(vstring)

        if not match:
            raise ValueError("invalid version number '%s'" % vstring)
        else:
            dev_num_index = len(match.groups())
            if match.group(dev_num_index):
                self.dev = string.atoi(match.group(dev_num_index))
            vstring = match.group(1)

        StrictVersion.__init__(self, vstring)

    def _increase_version(self, level=1, index=0):
        old_version = self.version

        old_comp = old_version[index]
        new_comp = old_comp + level

        new_version = []

        for i, comp in enumerate(old_version):
            if i == index:
                new_version.append(new_comp)
            else:
                new_version.append(old_version[i])

        self.version = tuple(new_version)

    def increase_major(self, level=1):
        self._increase_version(level, 0)

    def increase_minor(self, level=1):
        self._increase_version(level, 1)

    def increase_patch(self, level=1):
        self._increase_version(level, 2)

    def increase_dev(self, level=1):
        self.dev += level

    def __str__(self):
        prefix = StrictVersion.__str__(self)
        suffix = 'dev{ver}'.format(ver=self.dev)

        return '{prefix}{suffix}'.format(prefix=prefix, suffix=suffix)


