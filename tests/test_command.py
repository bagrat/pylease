from unittest import TestCase
from mock import patch, MagicMock, call
from nose.tools import ok_, eq_
from pylease.ex import PyleaseError
from pylease import Pylease
from pylease.util import SubclassIgnoreMark
from pylease.command import Command, NamedCommand
from pylease.command.task import BeforeTask, AfterTask
from pylease.vermgmt import InfoContainer


class CommandTest(TestCase):
    def test_command_global_init_should_ignore_marked_commands(self):
        inited = []

        class C0(Command):
            def __init__(self, dummy):
                super(C0, self).__init__(dummy, 'C0', 'C0 description')

                inited.append(self.__class__)

            def _process_command(self, lizy, args):
                pass

            def _get_name(self):
                pass

        class C1(C0):
            ignore_me = SubclassIgnoreMark('C1')

        class C2(C1):
            pass

        cmd_subparser = MagicMock()
        cmd_subparser.add_parser = MagicMock()
        Command.init_all(Pylease(None, cmd_subparser, None))

        ok_(C0 in inited)
        ok_(C1 not in inited)
        ok_(C2 in inited)

    def test_named_command_class_should_set_command_name_if_not_defined(self):
        description = 'some description'

        class SomeCommand(NamedCommand):
            def __init__(self, lizy):
                super(SomeCommand, self).__init__(lizy, description)

            def _process_command(self, lizy, args):
                return None, None

        subparser_mock = lambda: 0
        subparser_mock.add_parser = MagicMock()

        no_name = SomeCommand(Pylease(None, subparser_mock, None))

        eq_(no_name.name, 'some')
        subparser_mock.add_parser.assert_called_once_with('some', help=description)

    def test_calling_command_instance_should_fire_process_command_method(self):
        class C(Command):
            def __init__(self, lizy):
                super(C, self).__init__(lizy, 'C', 'C description')

            def _process_command(self, lizy, args):
                return None, None

        with patch.object(C, '_process_command') as process_command:
            process_command.return_value = None, None

            subparser_mock = lambda: 0
            subparser_mock.add_parser = MagicMock()
            info_container = InfoContainer()
            info_container.is_empty = False
            lizy = Pylease(None, subparser_mock, info_container)
            c = C(lizy)
            c(None)

            process_command.assert_called_once_with(lizy, None)

    def test_init_all_should_add_all_commands_to_lizy(self):
        class Base(NamedCommand):
            def __init__(self, lizy, description):
                super(Base, self).__init__(lizy, description)

            ignore_me = SubclassIgnoreMark('Base')

            def _process_command(self, lizy, args):
                pass

        class A(Command):
            NAME = 'A'
            DESC = 'A desc'

            def __init__(self, lizy):
                super(A, self).__init__(lizy, self.NAME, self.DESC)

            def _process_command(self, lizy, args):
                pass

        class BCommand(Base):
            NAME = 'B'
            DESC = 'B desc'

            def __init__(self, lizy):
                super(BCommand, self).__init__(lizy, self.DESC)

        class CCommand(Base):
            NAME = 'C'
            DESC = 'C desc'

            def __init__(self, lizy):
                super(CCommand, self).__init__(lizy, self.DESC)

        subparser_mock = lambda: 0
        subparser_mock.add_parser = MagicMock()

        lizy = Pylease(None, subparser_mock, None)
        Command.init_all(lizy)

        calls = [call(A.NAME, help=A.DESC), call(BCommand.NAME.lower(), help=BCommand.DESC),
                 call(CCommand.NAME.lower(), help=CCommand.DESC)]
        subparser_mock.add_parser.assert_has_calls(calls, any_order=True)

    def test_command_must_execute_before_tasks_before_self_execution(self):
        class SuccessCommand(NamedCommand):
            def __init__(self, lizy):
                super(SuccessCommand, self).__init__(lizy, 'desc')

            def _process_command(self, lizy, args):
                return None, None

        before = MagicMock()
        after = MagicMock()

        lizy = MagicMock()
        args = MagicMock()

        info_container = InfoContainer()
        info_container.is_empty = False

        lizy.info_container = info_container

        sc = SuccessCommand(lizy)

        sc.add_before_task(before)
        sc.add_after_task(after)

        sc(args)

        before.assert_called_once_with(lizy, args)
        after.assert_called_once_with(lizy, args)

    def test_command_must_not_execute_after_tasks_in_case_of_failure(self):
        class FailureCommand(NamedCommand):
            def __init__(self, lizy):
                super(FailureCommand, self).__init__(lizy, 'desc')

            def _process_command(self, lizy, args):
                raise PyleaseError()

        before = MagicMock()
        after = MagicMock()

        lizy = MagicMock()
        args = MagicMock()

        info_container = InfoContainer()
        info_container.is_empty = False
        lizy.info_container = info_container

        sc = FailureCommand(lizy)

        sc.add_before_task(before)
        sc.add_after_task(after)

        sc(args)

        before.assert_called_once_with(lizy, args)
        ok_(not after.called)

    def test_all_actions_must_be_rolled_back_on_failure(self):
        before_rollback = MagicMock()
        command_rollback = MagicMock()
        after_rollback = MagicMock()

        class RollbackTestCommand(NamedCommand):
            def __init__(self, lizy):
                super(RollbackTestCommand, self).__init__(lizy, 'rollback desc', command_rollback)

            def _process_command(self, lizy, args):
                return None

        class B(BeforeTask):
            def __init__(self):
                super(B, self).__init__(before_rollback)
                self.enable_rollback(before_rollback)

            def execute(self, lizy, args):
                pass

        class A(AfterTask):
            def __init__(self):
                super(A, self).__init__(after_rollback)
                self._needs_rollback = True

            def execute(self, lizy, args):
                raise PyleaseError()

        subparser_mock = lambda: 0
        subparser_mock.add_parser = MagicMock()

        info_container = InfoContainer()
        info_container.is_empty = False
        lizy = Pylease(None, subparser_mock, info_container)
        command = RollbackTestCommand(lizy)

        command.add_before_task(B())
        command.add_after_task(A())

        command(None)

        before_rollback.assert_called_once_with()
        command_rollback.assert_called_once_with()
        after_rollback.assert_called_once_with()
