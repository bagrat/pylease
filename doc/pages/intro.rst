Introduction
============

Pylease works on Python projects that are being managed by `setuptools <https://pypi.python.org/pypi/setuptools>`_,
i.e. have ``setup.py`` file in their root directory. This is enough to make Pylease get things done. Pylease is an extensible modular
tool, which enables the developers to enhance it further. So let us start with the installation first.

Installation
------------

Pylease is a regular Python package which comes with a command line tool, obviously called ``pylease``. So to start::

    $ pip install pylease

And then just check if everything went fine:

.. parsed-literal::

    $ pylease --version
    Pylease version \ |version|\

Workflow
--------

The simplicity of Pylease is that it does not require any specific configuration or scripts, it accepts Python projects just as-is.
Although, you can configure Pylease to fully use its features, it is not required and you can just start using Pylease on a project you
were working on for years. So let us consider two scenarios.

Project from Scratch
********************

So to start a new Python project, just create a new empty directory for your project and then use the ``init`` command to create a skeleton
for your project::

    $ mkdir my_project
    $ cd my_project
    $ pylease init my_project

Now you have the skeleton of your project ready to be used::

    $ ls -LR
    my_project setup.cfg  setup.py

    ./my_project:
    __init__.py
    $ cat setup.py
    import my_project
    from setuptools import setup

    setup(name='my_project',
          version=my_project.__version__)
    $ cat setup.cfg
    [pylease]
    version-files = my_project/__init__.py
    $ cat my_project/__init__.py
    __version__ = '0.0'

.. _existingProject:
Existing Project
****************

If you have an already initialised Python project, then the first thing you will want to do for feeling the presence of Pylease,
is the following::

    $ cd /path/to/your/project/root
    $ ls
    ... setup.py ...
    $ pylease status
    Project Name: <your project>
    Current Version: <project version>

Releasing a Project
*******************

The idea of Pylease came while doing some routine tasks during a release process of a Python project, thus the main focus of it is the
release process itself. So Pylease provides the ``make`` command to perform an appropriate release. But before doing anything release
related, first check out your current status as it is done for an `Existing Project`_.

So while you are working on a project, the current version defined is the last version the project was released with. As you can see in
initialising a `Project from Scratch`_, the initial version is ``0.0``, i.e. no release is done yet.

You may ask a reasonable question, why does not the current version represent the version you want to release next? The reason for that is
that it is possible that while working on the project, you might have a minor bug, small feature that will need a rapid release, so you
will need to make a ``patch`` or ``minor`` level release.

As already mentioned, you perform a release with the help of the ``make`` command of Pylease. The main and required parameter of ``make``
command is the release level, which is passed as one of the following:

 - ``--major``
 - ``--minor``
 - ``--patch``
 - ``--dev``

For instance, executing ``pylease make --minor`` on a project with version ``0.3`` will update it to ``0.4``::

    $ pylease status
    Project Name: example
    Current Version: 0.3
    $ pylease make --minor
    $ pylease status
    Project Name: example
    Current Version: 0.4

So this is pretty much all what the release is. As a result, you will have your ``setup.py`` updated to the new version. To customize the
behaviour of the release process, you might want to take a look at `Pylease configuration <config.html>`_.

Moreover, if you wish to add your own custom actions to Pylease, you should definitely get into `extending Pylease <ext.html>`_.

For a quick reference, always consider to take a look at ``--help`` messages for commands, e.g. ``pylease make --help``.
