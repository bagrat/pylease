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
from pylease.vermgmt import VersionContainer

__author__ = 'bagrat'


def _init_arg_parser():
    parser = ArgumentParser()

    root_group = parser.add_mutually_exclusive_group(required=False)

    version_group = root_group.add_argument_group(title='other arguments', description='aaa')
    version_group.add_argument('--version', dest='ver_req', action='store_const', const=True, help='Get Pylease version')

    release_group = root_group.add_argument_group(title='release arguments',
                                                  description='Specify one of those arguments to make the corresponding level release')

    level_group = release_group.add_mutually_exclusive_group(required=False)
    level_group.add_argument('--major', dest='level', action='store_const', const='major', help='Make a major release')
    level_group.add_argument('--minor', dest='level', action='store_const', const='minor', help='Make a minor release')
    level_group.add_argument('--patch', dest='level', action='store_const', const='patch', help='Make a patch release')
    level_group.add_argument('--dev', dest='level', action='store_const', const='dev', help='Make a dev release')

    return parser


def main():
    parser = _init_arg_parser()

    extensions = Extension.init_all([GitExtension], parser)

    args, setuptools_args = parser.parse_known_args()

    if args.ver_req:
        print(version_info())
        return 0

    level = args.level

    sys.argv = ['setup.py', 'sdist', 'upload'] + setuptools_args
    sys.path = [os.getcwd()] + sys.path

    vc = VersionContainer()
    with ReplacedSetup(vc.set_version):
        __import__('setup')

    old_version = vc.version
    new_version = release(old_version, level)

    count = update_files(old_version, new_version)
    if count == 0:
        logme.error("Version specification not found!")
        return 1
    elif count > 1:
        logme.warn("More than one version specification found.")

    vr = VersionRollback(old_version, new_version)
    with Caution(vr):
        __import__('setup')

    Extension.execute_all(extensions, args, new_version)


def version_info():
    version_str = "Pylease version {version}"
    version = pylease.__version__

    return version_str.format(version=version)
