Class Reference
===============

.. automodule:: pylease

    .. autoclass:: Pylease

    .. autoclass:: InfoContainer

        .. automethod:: set_info



.. automodule:: pylease.ext

    .. autoclass:: Extension

        .. automethod:: load

.. automodule:: pylease.cmd.task

    .. autoclass:: BeforeTask

        .. automethod:: execute

    .. autoclass:: AfterTask

        .. automethod:: execute

        .. autoattribute:: _command_result

.. automodule:: pylease.cmd

    .. autoclass:: Command

        .. automethod:: __init__

        .. automethod:: _process_command

        .. automethod:: add_before_task

        .. automethod:: add_after_task

    .. autoclass:: NamedCommand

        .. automethod:: __init__
