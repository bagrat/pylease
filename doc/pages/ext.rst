Extending Pylease
=================

Although Pylease is an Open Source project, it is impossible to consider and include all possible features at once. Moreover, one may
want a particular feature urgently. Even after sending a feature request, he may have no time to wait for confirmation, implementation
and release of that feature. On the other hand, Pylease may get too much loaded with features that does not get used by everyone.

For this reason, one of the major parts of Pylease is its extension system. It allows to develop a separate Python pakage and optionally
plug it into Pylease.

So basically there are two ways to extend Pylease:

 - Add before and after tasks for existing commands
 - Add new commands

In the last subsection you will find a detailed tutorial on both options for extending Pylease.

Extending Existing Commands
---------------------------

Here is the step-by-setp guide on how to add extensions to Pylease.

The first step is inheriting the :class:`~pylease.ext.Extension` class, where you will place the initialisation code by implementing the
:func:`~pylease.ext.Extension.load` method. As an instance attribute you will have the :attr:`~pylease.ext.Extension._lizy` attribute,
which is an instance of :class:`~pylease.Pylease` class, and contains everything you need for your extension.

Extending an existing Pylease command is done by adding a :class:`~pylease.cmd.task.BeforeTask` or :class:`~pylease.cmd.task.AfterTask`
(or both) to it. What is needed to do is just implement those classes and add their instances to the command that is the subject of
extension. For both :class:`~pylease.cmd.task.BeforeTask` and :class:`~pylease.cmd.task.AfterTask` you need to inherit and implement
their :func:`~pylease.cmd.task.BeforeTask.execute` method, which must include the extension logic. Also, in case of
:class:`~pylease.cmd.task.AfterTask`, you are provided with the :attr:`~pylease.cmd.task.AfterTask._command_result` attribute, which is
the result returned by the command being extended.

So basically this is the scenario of extending a Pylease command:

 - Inherit and implement :class:`~pylease.cmd.task.BeforeTask` or/and :class:`~pylease.cmd.task.AfterTask`
 - Inherit :class:`~pylease.ext.Extension`
 - In the :func:`~pylease.ext.Extension.load` implementation get the corresponding :class:`~pylease.cmd.Command` instance from the
   :attr:`~pylease.ext.Extension._lizy` singleton
 - Add the :class:`~pylease.cmd.task.BeforeTask` or/and :class:`~pylease.cmd.task.AfterTask` instances to the command instance

Adding New Commands
-------------------

To add a new command to Pylease it is enough to implement a class by inheriting the :class:`~pylease.cmd.Command` class and add it to your
package
``__init__.py``.
