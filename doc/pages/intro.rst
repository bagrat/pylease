Introduction
============

Pylease works on Python projects that are being managed by `setuptools <https://pypi.python.org/pypi/setuptools>`_,
i.e. have ``setup.py`` file in their root directory. This is enough to make Pylease get things done.

Installation
------------

Pylease is a regular Python package which comes with a command line tool, obviously called ``pylease``. So to start::

    $ pip install pylease

And then just check if everything went fine::

    $ pylease --version


Workflow
--------

The simplicity of Pylease is that it does not require any specific configuration or scripts, it accepts Python projects just as-is.
Although, you can configure Pylease to fully use its features, it is not required and you can just start using Pylease on a project you
were working on for years. So let us consider two scenarios.

Project from Scratch
********************

So to start a new Python project, just create a new empty directory for your project and then use the `init` command to create a skeleton
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
    __version__ = '0.1'

Existing Project
****************

If you have an already initialized Python project, then the first thing you will want to do for feeling the presence of Pylease,
is the following::

    $ cd /path/to/your/project/root
    $ ls
    ... setup.py ...
    $ pylease status
    Project Name: <your project>
    Current Version: <project version>

