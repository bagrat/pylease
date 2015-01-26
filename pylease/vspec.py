from pylease.util import get_caller_module

__author__ = 'bagrat'


# This class should be the only class in this file
class version(str):
    """
    Version specification class which will be used in setup.py.

    The version specification statement can be written as a simple
    instantiation of this class, i.e. ``version('1.0')``. Next, The value
    can be obtained for supplying to setup method by just referring to the
    class name, i.e. ``setup(version=version)``.
    """
    @classmethod
    def __new__(cls, *args, **kwargs):
        obj = super(version, cls).__new__(*args)

        var_name = kwargs.get('var_name', None)
        if not var_name:
            var_name = cls.__name__

        module = get_caller_module(1)
        module.__dict__[var_name] = obj

        return obj
