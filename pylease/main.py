import os
import sys
from pylease.caution import DirtyCaution, ReplacedSetup
from pylease.ex import VersionRetrievalError

__author__ = 'bagrat'

from optparse import OptionParser
from releasemgmt import default_level, release

_parser = OptionParser(
    usage="pylease [major | minor | patch | dev] [setuptools_args]")

_parser.add_option('--dev', action="store_const", dest='level',
                   const='dev', default=default_level)
_parser.add_option('--patch', action="store_const", dest='level',
                   const='patch', default=default_level)
_parser.add_option('--minor', action="store_const", dest='level',
                   const='minor', default=default_level)
_parser.add_option('--major', action="store_const", dest='level',
                   const='major', default=default_level)


def main():
    rest_argv = sys.argv
    if len(sys.argv) > 1:
        sys.argv = sys.argv[0:2]

    (options, _) = _parser.parse_args()

    level = options.level

    sys.argv = ['setup.py', 'sdist', 'upload'] + rest_argv[2:]

    sys.path = [os.getcwd()] + sys.path

    with ReplacedSetup():
        try:
            __import__('setup')
        except VersionRetrievalError as ex:
            current_version = ex.version

    release(current_version, level)

    with DirtyCaution(current_version):
        __import__('setup')
