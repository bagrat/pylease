import os
import sys
from argparse import ArgumentParser

import logger
import pylease
from pylease.extension import Extension
from pylease.extension import git, pypi  # noqa
from pylease.command import Command
from pylease.ctxmgmt import ReplacedSetup
from pylease.vermgmt import InfoContainer

__author__ = 'bagrat'


def main(args=None):

    # Initialize argument parser
    parser = ArgumentParser()
    parser.add_argument('--version', action='version', version=version_info())
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        dest='verbose',
                        default=False,
                        help='Make Pylease verbose, i.e. show more execution information')
    sub_parsers = parser.add_subparsers(help='Pylease commands', dest='command')

    sys.path = [os.getcwd()] + sys.path
    info = InfoContainer()
    with ReplacedSetup(info.set_info):
        __import__('setup')

    lizy = pylease.Pylease(parser, sub_parsers, info)

    Command.init_all(lizy)
    Extension.init_all(lizy)

    args = parser.parse_args(args)

    if args.verbose:
        logger.add_verbose_handler()

    command_name = args.command

    return lizy.execute_command(command_name, args)


def version_info():
    version_str = "Pylease version {version}"
    version = pylease.__version__

    return version_str.format(version=version)
