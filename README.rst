Pylease
=======

.. image:: https://landscape.io/github/n9code/pylease/dev/landscape.svg?style=flat
   :target: https://landscape.io/github/n9code/pylease/dev
   :alt: Code Health

Pylease is a simple package that tends to ease the release process of a regular Python package. The aim of Pylease is to make it as
simple as possible by requiring as little as possible. For more details on using Pylease please see the `documentation <http://n9code
.github.io/pylease/>`_.

Basic Usage
-----------

Start using pylease by just navigating to you package root (the directory containing
``setup.py``) and simply use the command-line::

    $ pylease --dev

This will release the package with version '1.0.dev1', i.e. update the
version in setup.py and upload it to PyPi. If you need to customize the
behaviour of setuptools (e.g. by uploading your package to another
repository), you may pass any other setuptools command-line arguments to
pylease::

    $ pylease --major -r other_repo

The release levels include ``major, minor, patch and dev``.

Extensions
----------

Pylease also includes some useful extensions that might be used in combination.

Git
~~~

Git extension provides functionality to automatically create a tag on the
git repository associated with the version, and commit the changes made to
the ``setup.py``.

This may be achieved by simply adding ``--git-tag`` argument while calling
pylease::

    $ pylease --minor --git-tag

After making the release, you will additionally have a new commit
containing the setup.py update as well as a new tag pointing to that commit.