Pylease Configuration
=====================

As you have already `seen <intro.html#existing-project>`__, Pylease works on an existing project without requiring any configuration.
However, at some point in time you will need to make some configuration to use Pylease fully. The place for Pylease configuration is the
``setup.cfg`` file of your project, under the ``[pylease]`` section. Here is an example configuration:

**setup.cfg**::

    ...

    [pylease]
    version-files = my_project/__init__.py

    ...

Following is the list of all configuration parameters with their descriptions.

.. _version-files:
``version-files``
    A list of files where the version must be updated to the new one. Here is an example value for this parameter:

        ``version-files = my_project/__init__.py, setup.py``

.. _use-plugins:
``use-plugins``
    A list of external plugins to load. If you have installed ``example_plugin`` package in your Python environment, and want Pylease to
    use that plugin, you just need to add the ``example_plugin`` name to the list of this parameter.

