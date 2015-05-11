from mock import MagicMock
from nose.tools import eq_, ok_
from pylease.command.rollback import Rollback, Stage
from tests import PyleaseTest

stage1 = 'stage1'
stage1_priority = 0
stage2 = 'stage2'
stage2_priority = 2
stage3 = 'stage3'
stage3_priority = 1
stage1_mock = MagicMock()
stage2_mock = MagicMock()
stage3_mock = MagicMock()
stage_execution_queue = []


class RollbackTest(PyleaseTest):
    def setUp(self):  # noqa
        super(RollbackTest, self).setUp()
        global stage_execution_queue

        stage_execution_queue = []

    class SomeRollback(Rollback):
        @Stage(stage1, stage1_priority)
        def stage1_rollback(self):
            stage1_mock()
            stage_execution_queue.append(stage1_mock)

        @Stage(stage2, stage2_priority)
        def stage2_rollback(self):
            stage2_mock()
            stage_execution_queue.append(stage2_mock)

        @Stage(stage3, stage3_priority)
        def stage3_rollback(self):
            stage3_mock()
            stage_execution_queue.append(stage3_mock)

    def test_rollback_mechanism_should_generate_appropriate_dictionary(self):
        rollback = self.SomeRollback()

        expected_stages = {stage1: {rollback.stage1_rollback: (stage1_priority, False)},
                           stage2: {rollback.stage2_rollback: (stage2_priority, False)},
                           stage3: {rollback.stage3_rollback: (stage3_priority, False)}}

        eq_(expected_stages, rollback._stages)

    def test_it_must_be_possible_to_cherry_pick_enable_rollback_stages(self):
        rollback = self.SomeRollback()

        rollback.enable_stage(stage2)

        ok_(rollback._stages[stage2][rollback.stage2_rollback][1])
        ok_(not rollback._stages[stage1][rollback.stage1_rollback][1])

    def test_rollback_mechanism_should_execute_enabled_stages_in_correct_order(self):
        rollback = self.SomeRollback()

        rollback.enable_stage(stage2)
        rollback.enable_stage(stage3)
        rollback.rollback()

        ok_(stage1_mock not in stage_execution_queue)
        stage2_mock.assert_called_once_with()
        stage3_mock.assert_called_once_with()

        stage2_index = stage_execution_queue.index(stage2_mock)
        stage3_index = stage_execution_queue.index(stage3_mock)

        ok_(stage2_index < stage3_index)
