Extending Pylease
=================

Although Pylease is an Open Source project, it is impossible to consider and include all possible features at once. Moreover, one may
want a particular feature urgently. Even after sending a feature request, he may have no time to wait for confirmation, implementation
and release of that feature. On the other hand, Pylease may get too much loaded with features that does not get used by everyone.

For this reason, one of the major parts of Pylease is its modular extension system. It allows to develop a separate Python pakage and
optionally
plug it into Pylease.

So basically there are two ways to extend Pylease:

 - Add before and after tasks for existing commands
 - Add new commands

The following two subsections discuss both scenarios with their details.

Extending Existing Commands
---------------------------

Here is the step-by-setp guide on how to add extensions to Pylease.

The first step is inheriting the :class:`~pylease.ext.Extension` class and adding it to your package ``__init__.py``, where you will place
the initialisation code by implementing the :func:`~pylease.ext.Extension.load` method. As an instance attribute you will have the
:attr:`~pylease.ext.Extension._lizy` attribute, which is an instance of :class:`~pylease.Pylease` class, and contains everything you need
for your extension.

Extending an existing Pylease command is done by adding a :class:`~pylease.cmd.task.BeforeTask` or :class:`~pylease.cmd.task.AfterTask`
(or both) to it using the :class:`~pylease.cmd.Command` methods :func:`~pylease.cmd.Command.add_before_task` and
:func:`~pylease.cmd.Command.add_after_task`. What is needed to do is just implement those classes and add their instances to the command
that is the subject of extension. For both :class:`~pylease.cmd.task.BeforeTask` and :class:`~pylease.cmd.task.AfterTask` you need to
inherit and implement their :func:`~pylease.cmd.task.BeforeTask.execute` method, which must include the extension logic. Also, in case of
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
package ``__init__.py``. Implementing the :class:`~pylease.cmd.Command` class is implementing the
:func:`~pylease.cmd.Command._process_command` method. As an additional convenience you can inherit the :class:`~pylease.cmd.NamedCommand`
class instead. This will eliminate the need to manually specify the name of the command while calling the base constructor. Instead this
base class will automatically parse the command name from the class name by removing the "\ |pylease_named_command_suffix|\ " suffix and using the rest as the
command name. So for example, the ``init`` command is defined as a child class of :class:`~pylease.cmd.NamedCommand` with the name
``InitCommand``.

As in the case of implementing :class:`~pylease.ext.Extension`, here you will also be provided with the :class:`~pylease.Pylease`
``lizy`` singleton.

Rollbacks
---------

Even if you ship a perfectly clear extension, which will never crash in any conditions, you have no guarantee for others. As Pylease is a
modular tool, it is possible to plug any number of independent extensions. This means that it is possible that after your extension task or
command is executed, there may be another task executed after, that will lead to an error. In this case, you might need to rollback all
the changes that your extension made to maintain the original state of the project.

For instance, the `Git plugin <plugin.html#git>`_ makes a commit for the changes of version of the project, then creates a tag for the
version. If any error raises after this operations, is it critical to roll them back. Thus, this plugin deletes the last commit and
removes the created tag.

Pylease provides the :class:`~pylease.cmd.rollback.Rollback` class and :class:`~pylease.cmd.rollback.Stage` decorator to implement this
feature in your extension. The :class:`~pylease.cmd.rollback.Stage` decorator enables to have a staged rollback. For example, in case of
the `Git plugin <plugin.html#git>`_, if the error occurres in the stage of creating the version tag, the only rollback step to perform is
deleting the last commit.

For reference on using this classes please see the `Class Reference <ref.html>`_ for :class:`~pylease.cmd.rollback.Rollback` and
:class:`~pylease.cmd.rollback.Stage`
