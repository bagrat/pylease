Built-in Plugins
================

As you will see in the `Extensing Pylease <ext.html>`__ section, you can customize and extend Pylease the way you like. Fortunately,
Pylease comes batteries included, with built-in plugins for most common tasks. Now let us take a look at each plugin separatelly.

Git
---

Pylease support integration with git. You can enable this plugin with the ``--git-tag`` option of the ``make`` command. Consider the
following situation::

    $ pylease status
    Project Name: example
    Current Version: 0.3
    $ git tag -l
    v0.1
    v0.1.1
    v0.2
    v0.3

As you can see the **example** project has four releases - ``0.1``, ``0.1.1``, ``0.2``, ``0.3``, and current version is ``0.3``. So
imagine you want to make a ``patch`` release and create appropriate tag in your git repository::

    $ pylease make --patch --git-tag
    $ pylease status
    Project Name: example
    Current Version: 0.3.1
    $ git tag -l
    v0.1
    v0.1.1
    v0.2
    v0.3
    v0.3.1


PyPI
----

The Pylease PyPI plugin enables to automatically upload your package egg to PyPI. The only prerequisite for this action is that the
package name must be already registered, as well as you must be responsible for authentication over the `.pypirc <https://docs.python
.org/2/distutils/packageindex.html#pypirc>`__ file.

To enable this feature during the release process you should just use the ``--pypi`` option like this::

    $ pylease make --major --pypi

This ``--pypi`` part of this command simply does the same as the ``python setup.py sdist upload``.
