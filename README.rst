Pylease
=======

Pylease is a simple package that tends to ease the release process of a regular
Python package. The aim of Pylease is to make it as simple as possible by
requiring as little as possible.

Basic Usage
-----------

The only requirement of Pylease is to place a Version Specification in the
setup.py of your package before calling the setup method. This may be done in
the following trivial way::

    # setup.py

    from pylease import version

    # and here comes the Version Specification
    version('1.0')

    ...

    setup(name="myproject", version=version)


What? Yes, simply call ``version('1.0')`` and then refer the version as a
string with the same name.

After having the Version Specification in your setup.py, you are ready for
making releases with pylease command-line tool, by simply providing the
release level::

    $ pylease dev

This will release the package with version '1.0.dev1', i.e. update the
version in setup.py and upload it to PyPi. If you need to customize the
behaviour of setuptools (e.g. by uploading your package to another
repository), you may pass any other setuptools command-line arguments to
pylease::

    $ pylease major -r other_repo

The release levels include ``major, minor, patch and dev``.