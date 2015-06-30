

class Rollback(object):
    """
    This class provides a facility to define a staged rollback process. The scenario of using this class is the following:

        #. Inherit :class:`~pylease.cmd.rollback.Rollback` class
        #. Define rollback stages as instance methods
        #. Decorate each rollback method with :class:`~pylease.cmd.rollback.Stage` decorator, by specifying stage name and priority
        #. Enable each stage separately calling :func:`~pylease.cmd.rollback.Rollback.enable_stage` method
    """
    def __init__(self):
        super(Rollback, self).__init__()

        self._stages = {}

        for rollback in dir(self):
            rollback_obj = getattr(self, rollback)
            if hasattr(rollback_obj, Stage.STAGE_ATTR_NAME):
                stage = getattr(rollback_obj, Stage.STAGE_ATTR_NAME)
                priority = getattr(rollback_obj, Stage.PRIORITY_ATTR_NAME)

                if not self._stages.get(stage):
                    self._stages[stage] = {}

                self._stages[stage][rollback_obj] = (priority, False)  # (priority, enabled)

    def rollback(self):
        """
        Execute all rollback stages ordered by priority.
        """
        rollbacks = []
        for stage in self._stages:
            for rollback in self._stages[stage]:
                priority, enabled = self._stages[stage][rollback]

                if enabled:
                    rollbacks.append((stage, priority, rollback))

        rollbacks = sorted(rollbacks, key=lambda obj: obj[1], reverse=True)

        for rollback in rollbacks:
            rollback[2]()

    def enable_stage(self, stage):
        """
        Enable particular stage by name.

        Arguments:
            stage (str): Stage name to enable.
        """
        rollbacks = self._stages[stage]

        for rollback in rollbacks:
            priority, _ = self._stages[stage][rollback]
            self._stages[stage][rollback] = (priority, True)

    def __call__(self):
        self.rollback()  # pragma: no cover - For simple use and convenience


class Stage(object):
    # pylint: disable=too-few-public-methods
    """
    Decorator used in custom :class:`~pylease.cmd.rollback.Rollback` classes for associating each method with a stage, and setting priority.

    Arguments:
        stage (str): The name of the stage.
        priority (int): The order priority of the stage to be rolled back. Defaults to ``0``.

    Example:
        Here is an example of how to use the :class:`~pylease.cmd.rollback.Stage` decorator in combination with the
        :class:`~pylease.cmd.rollback.Rollback` base class::

            class ExampleRollback(Rollback):
                @Stage('some_stage', 1)
                def some_stage_with_priority_1(self):
                    pass  # your some_stage rollback goes here

    """
    STAGE_ATTR_NAME = '_stage'
    PRIORITY_ATTR_NAME = '_priority'

    def __init__(self, stage, priority=0):
        super(Stage, self).__init__()

        self._stage = stage
        self._priority = priority

    def __call__(self, func):
        setattr(func, self.STAGE_ATTR_NAME, self._stage)
        setattr(func, self.PRIORITY_ATTR_NAME, self._priority)

        return func
