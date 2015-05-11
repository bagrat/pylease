

class Rollback(object):
    """
    This class provides a facility to define a staged rollback process. The scenario of using this class is the following:

    1. Inherit Rollback class
    2. Define rollback stages as instance methods
    3. Decorate each rollback method with `Stage` decorator, by specifying stage name and priority
    4. Enable each stage separately calling `enable_stage` method
    5. Call `rollback` method, which will execute all enabled rollback stages, ordered by priority
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
        :param stage: Stage name
        :return:
        """
        rollbacks = self._stages[stage]

        for rollback in rollbacks:
            priority, _ = self._stages[stage][rollback]
            self._stages[stage][rollback] = (priority, True)

    def __call__(self):
        self.rollback()  # pragma: no cover - For simple use and convenience


class Stage(object):
    """
    Decorator used in custom `Rollback` classes for associating each method with a stage, and setting priority
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
