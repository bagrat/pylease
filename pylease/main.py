import os
import sys
from argparse import ArgumentParser

import pylease
from pylease.extension import Extension
from pylease.extension import git  # noqa
from pylease.command import Command
from pylease.ctxmgmt import ReplacedSetup
from pylease.vermgmt import InfoContainer

__author__ = 'bagrat'


def main(args=None):

    # Initialize argument parser
    parser = ArgumentParser()
    parser.add_argument('--version', action='version', version=version_info())
    sub_parsers = parser.add_subparsers(help='Pylease commands', dest='command')

    sys.path = [os.getcwd()] + sys.path
    info = InfoContainer()
    with ReplacedSetup(info.set_info):
        __import__('setup')

    lizy = pylease.Pylease(parser, sub_parsers, info)

    Command.init_all(lizy)
    Extension.init_all(lizy)

    args = parser.parse_args(args)

    command_name = args.command

    return lizy.execute_command(command_name, args)

    #
    #
    # vr = VersionRollback(old_version, new_version)
    # with Caution(vr):
    #     __import__('setup')


def version_info():
    version_str = "Pylease version {version}"
    version = pylease.__version__

    return version_str.format(version=version)
