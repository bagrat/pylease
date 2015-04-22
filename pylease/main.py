import os
import sys
from argparse import ArgumentParser

import pylease
from pylease import logme
from pylease.ctxmgmt import ReplacedSetup, Caution
from pylease.extension import Extension
from pylease.extension.git import GitExtension
from pylease.filemgmt import update_files, VersionRollback
from pylease.releasemgmt import release
from pylease.vermgmt import InfoContainer

__author__ = 'bagrat'


def _init_arg_parser():
    parser = ArgumentParser()

    parser.add_argument('--version', action='version', version=version_info())

    sub_parsers = parser.add_subparsers(help='Pylease commands', dest='command')

    release_parser = sub_parsers.add_parser('make', help='Retrieve current status of the project')

    release_group = release_parser.add_argument_group(title='release arguments',
                                                      description='Specify one of those arguments to make the '
                                                      'corresponding level release')

    level_group = release_group.add_mutually_exclusive_group(required=False)
    level_group.add_argument('--major', dest='level', action='store_const', const='major', help='Make a major release')
    level_group.add_argument('--minor', dest='level', action='store_const', const='minor', help='Make a minor release')
    level_group.add_argument('--patch', dest='level', action='store_const', const='patch', help='Make a patch release')
    level_group.add_argument('--dev', dest='level', action='store_const', const='dev', help='Make a dev release')

    return parser


def main():
    sys.path = [os.getcwd()] + sys.path
    ic = InfoContainer()
    with ReplacedSetup(ic.set_info):
        __import__('setup')
    old_version = ic.version

    parser = _init_arg_parser()

    # lizy = pylease.Pylease(parser, ic.name, ic.version)

    extensions = Extension.init_all([GitExtension], parser)

    args, setuptools_args = parser.parse_known_args()

    print(args)

    level = args.level

    sys.argv = ['setup.py', 'sdist', 'upload'] + setuptools_args

    ic = InfoContainer()
    with ReplacedSetup(ic.set_info):
        __import__('setup')

    new_version = release(old_version, level)

    counts = update_files(old_version, new_version)
    if len(counts) == 0:
        logme.error("Version specification not found!")
        return 1
    elif len(counts) > 1:
        logme.warn("More than one version specification found.")
        logme.debug("Occurrences:")
        for filename in counts:
            logme.debug("\t{filename}: {count}".format(filename=filename, count=counts[filename]))

    vr = VersionRollback(old_version, new_version)
    with Caution(vr):
        __import__('setup')

    Extension.execute_all(extensions, args, new_version)


def version_info():
    version_str = "Pylease version {version}"
    version = pylease.__version__

    return version_str.format(version=version)
