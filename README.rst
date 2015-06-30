Pylease
=======

.. image:: https://travis-ci.org/n9code/pylease.svg?branch=master
    :target: https://travis-ci.org/n9code/pylease
    :alt: Build Status

.. image:: https://landscape.io/github/n9code/pylease/master/landscape.svg?style=flat
    :target: https://landscape.io/github/n9code/pylease/master
    :alt: Code Health


.. image:: https://coveralls.io/repos/n9code/pylease/badge.svg?branch=master
    :target: https://coveralls.io/r/n9code/pylease?branch=master
    :alt: Code Coverage

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/n9code/pylease/master/LICENSE
    :alt: License

Pylease is a simple package that tends to ease the release process of a regular Python package. The aim of Pylease is to make it as
simple as possible by requiring as little as possible. For more details on using Pylease please see the `documentation <http://pylease
.n9co.de>`_.

Basic Usage
-----------

Start using pylease by just navigating to you package root (the directory containing ``setup.py``) and simply use the command-line::

    $ pylease status

Now you will see basic information about your package, like name and version. Then take a try and do::

    $ pylease make --dev

This will release the package with version '1.0.dev1', i.e. update the version in setup.py. The release levels include ``major, minor,
patch and dev``.

If you want to initiate a branch new project, perform this::

    $ pylease init my_project

This will prepare and create all needed files and directories for your project skeleton.

Extensions
----------

Pylease also comes with extensions mechanisms. It includes some useful extensions that might be used in combination as well as anyone can
write extensions for Pylease to enhance it.

Git
~~~

Git extension provides functionality to automatically create a tag on the
git repository associated with the version, and commit the changes made to
the ``setup.py``.

This may be achieved by simply adding ``--git-tag`` argument while calling
pylease::

    $ pylease make --minor --git-tag

After making the release, you will additionally have a new commit
containing the setup.py update as well as a new tag pointing to that commit.

PyPI
~~~~

PyPI extension provides an ability to automatically upload you package distribution to `PyPi
<http://pypi.python.org>`_ after releasing your project. To enable this feature use the ``--pypi``
command line option::

    $ pylease make --major --pypi


