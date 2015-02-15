import os
import subprocess
import sys
from argparse import ArgumentParser

from pylease import logme
from pylease.ctxmgmt import ReplacedSetup, Caution
from pylease.extension import Extension
from pylease.extension.git import GitExtension
from pylease.filemgmt import update_setup_py, VersionRollback
from pylease.releasemgmt import release
from pylease.vermgmt import VersionContainer

__author__ = 'bagrat'


def _init_arg_parser():
    parser = ArgumentParser()

    release_group = parser.add_argument_group(title='release arguments',
                                              description='Specify one of those arguments to make the corresponding level release')

    level_group = release_group.add_mutually_exclusive_group(required=True)
    level_group.add_argument('--major', dest='level', action='store_const', const='major', help='Make a major release')
    level_group.add_argument('--minor', dest='level', action='store_const', const='minor', help='Make a minor release')
    level_group.add_argument('--patch', dest='level', action='store_const', const='patch', help='Make a patch release')
    level_group.add_argument('--dev', dest='level', action='store_const', const='dev', help='Make a dev release')

    return parser


def main():
    parser = _init_arg_parser()

    extensions = Extension.init_all([GitExtension], parser)

    args, setuptools_args = parser.parse_known_args()

    level = args.level

    sys.argv = ['setup.py', 'sdist', 'upload'] + setuptools_args
    sys.path = [os.getcwd()] + sys.path

    logme.info("Working")

    vc = VersionContainer()
    with ReplacedSetup(vc.set_version):
        __import__('setup')

    old_version = vc.version
    new_version = release(old_version, level)

    count = update_setup_py(old_version, new_version)
    if count == 0:
        logme.error("Version specification not found!")
        sys.exit(1)
    elif count > 1:
        logme.warn("more than one version specification found.")

    vr = VersionRollback(old_version, new_version)
    with Caution(vr):
        __import__('setup')

    Extension.execute_all(extensions, args, new_version)


class Rollback(VersionRollback):
    def __init__(self, old_version, new_version):
        super(Rollback, self).__init__(old_version, new_version)

    def rollback(self):
        super(Rollback, self).rollback()

        subprocess.call("pip uninstall pylease")

