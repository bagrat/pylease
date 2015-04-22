from unittest import TestCase
from mock import patch
from nose.tools import *
from pylease import Pylease
from pylease.util import SubclassIgnoreMark
from pylease.command import Command, NamedCommand


class CommandTest(TestCase):
    def test_command_global_init_should_ignore_marked_commands(self):
        inited = []

        class C0(Command):
            def __init__(self, dummy):
                super(C0, self).__init__(dummy)

                inited.append(self.__class__)

            def _process_command(self, lizy, args):
                pass

            def _get_name(self):
                pass

        class C1(C0):
            ignore_me = SubclassIgnoreMark('C1')

        class C2(C1):
            pass

        with patch.object(Command, '__init__') as init_mock:
            init_mock.return_value = None

            Command.init_all(None)

        ok_(C0 in inited)
        ok_(C1 not in inited)
        ok_(C2 in inited)

    def test_named_command_class_should_set_command_name_if_not_defined(self):
        class SomeCommand(NamedCommand):
            def _process_command(self, lizy, args):
                pass

        class SomeCommandWithDefinedName(NamedCommand):
            THE_NAME = 'the name'

            def _get_name(self):
                return self.THE_NAME

            def _process_command(self, lizy, args):
                pass

        with patch.object(Command, '__init__') as init_mock:
            init_mock.return_value = None

            no_name = SomeCommand(None)
            with_name = SomeCommandWithDefinedName(None)

        eq_(no_name.name, 'some')
        eq_(with_name.name, SomeCommandWithDefinedName.THE_NAME)

    def test_calling_command_instance_should_fire_process_command_method(self):
        class C(Command):
            def _process_command(self, lizy, args):
                pass

            def _get_name(self):
                pass

        with patch.object(Command, '__init__') as init_mock:
            with patch.object(C, '_process_command') as process_command:
                init_mock.return_value = None

                c = C(None)
                c._lizy = None
                c(None)

                process_command.assert_called_once_with(None, None)

    def test_init_all_should_add_all_commands_to_lizy(self):
        class Base(NamedCommand):
            ignore_me = SubclassIgnoreMark('Base')

            def _process_command(self, lizy, args):
                pass

        class A(Command):
            def _process_command(self, lizy, args):
                pass

            def _get_name(self):
                return 'A'

        class BCommand(Base):
            pass

        class CCommand(Base):
            pass

        lizy = Pylease(None, None, None, None)
        Command.init_all(lizy)
