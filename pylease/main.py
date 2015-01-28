from argparse import ArgumentParser
import os
import sys

from pylease.ctxmgmt import ReplacedSetup, DirtyCaution
from pylease.ex import VersionRetrievalError, VersionSpecError
from pylease.extension import Extension
from pylease.extension.git import GitExtension
from pylease.releasemgmt import release

__author__ = 'bagrat'


def main():
    parser = ArgumentParser()

    release_group = parser \
        .add_argument_group(title='release arguments',
                            description='Specify one of those arguments '
                                        'to make the corresponding level '
                                        'release')

    level_group = release_group.add_mutually_exclusive_group(required=True)
    level_group.add_argument('--major', dest='level', action='store_const',
                             const='major', help='Make a major release')
    level_group.add_argument('--minor', dest='level', action='store_const',
                             const='minor', help='Make a minor release')
    level_group.add_argument('--patch', dest='level', action='store_const',
                             const='patch', help='Make a patch release')
    level_group.add_argument('--dev', dest='level', action='store_const',
                             const='dev', help='Make a dev release')

    extensions = Extension.init_all([GitExtension], parser)

    args, setuptools_args = parser.parse_known_args()

    level = args.level

    sys.argv = ['setup.py', 'sdist', 'upload'] + setuptools_args

    sys.path = [os.getcwd()] + sys.path

    with ReplacedSetup():
        try:
            __import__('setup')
        except VersionRetrievalError as ex:
            current_version = ex.version

    try:
        new_version = release(current_version, level)
    except VersionSpecError:
        print("Error: setup.py must contain one version specification.")
        sys.exit(1)

    with DirtyCaution(current_version):
        __import__('setup')

    Extension.execute_all(extensions, args, new_version)
