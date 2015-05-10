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
    """
    The main entry point of Pylease utility. Called when Pylease is launched from command line. May also be called from another python
    package by just supplying command line arguments as a list.

    :param args: List of command line arguments
    :return: Error code indicating completion status
    """
    # Initialize argument parser
    parser = ArgumentParser()
    parser.add_argument('--version', action='version', version=version_info())
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        dest='verbose',
                        default=False,
                        help='Make Pylease verbose, i.e. show more execution information')
    sub_parsers = parser.add_subparsers(help='Pylease commands', dest='command')

    # Collect current information about the project
    sys.path = [os.getcwd()] + sys.path
    info = InfoContainer()
    with ReplacedSetup(info.set_info):
        __import__('setup')

    # Initialize Lizy
    lizy = pylease.Pylease(parser, sub_parsers, info)

    # Initialize Commands and Extensions
    Command.init_all(lizy)
    Extension.init_all(lizy)

    # Parse and handle arguments
    args = parser.parse_args(args)

    if args.verbose:
        logger.add_verbose_handler()

    command_name = args.command

    # Execute requested command and return error code
    return lizy.execute_command(command_name, args)


def version_info():
    """
    Generates output of Pylease version information, when it is called with --version argument

    :return: Version information string
    """
    version_str = "Pylease version {version}"
    version = pylease.__version__

    return version_str.format(version=version)
