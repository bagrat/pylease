import os
import sys
from argparse import ArgumentParser

import pylease
from pylease.command import Command
from pylease.ctxmgmt import ReplacedSetup
from pylease.vermgmt import InfoContainer

__author__ = 'bagrat'


def _init_arg_parser():

    # release_parser = sub_parsers.add_parser('make', help='Retrieve current status of the project')
    #
    # release_group = release_parser.add_argument_group(title='release arguments',
    #                                                   description='Specify one of those arguments to make the '
    #                                                   'corresponding level release')
    #
    # level_group = release_group.add_mutually_exclusive_group(required=False)
    # level_group.add_argument('--major', dest='level', action='store_const', const='major', help='Make a major release')
    # level_group.add_argument('--minor', dest='level', action='store_const', const='minor', help='Make a minor release')
    # level_group.add_argument('--patch', dest='level', action='store_const', const='patch', help='Make a patch release')
    # level_group.add_argument('--dev', dest='level', action='store_const', const='dev', help='Make a dev release')
    pass


def main(args=None):

    # Initialize argument parser
    parser = ArgumentParser()
    parser.add_argument('--version', action='version', version=version_info())
    sub_parsers = parser.add_subparsers(help='Pylease commands', dest='command')

    sys.path = [os.getcwd()] + sys.path
    ic = InfoContainer()
    with ReplacedSetup(ic.set_info):
        __import__('setup')

    lizy = pylease.Pylease(parser, sub_parsers, ic)

    Command.init_all(lizy)

    args = parser.parse_args(args)

    command_name = args.command

    lizy.execute_command(command_name, args)

    # level = args.level
    #
    # sys.argv = ['setup.py', 'sdist', 'upload'] + setuptools_args
    #
    # ic = InfoContainer()
    # with ReplacedSetup(ic.set_info):
    #     __import__('setup')
    #
    # new_version = release(old_version, level)
    #
    # counts = update_files(old_version, new_version)
    # if len(counts) == 0:
    #     logme.error("Version specification not found!")
    #     return 1
    # elif len(counts) > 1:
    #     logme.warn("More than one version specification found.")
    #     logme.debug("Occurrences:")
    #     for filename in counts:
    #         logme.debug("\t{filename}: {count}".format(filename=filename, count=counts[filename]))
    #
    # vr = VersionRollback(old_version, new_version)
    # with Caution(vr):
    #     __import__('setup')


def version_info():
    version_str = "Pylease version {version}"
    version = pylease.__version__

    return version_str.format(version=version)
