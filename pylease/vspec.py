__author__ = 'bagrat'

from pyflect.core.instor.instor import _get_caller_module


# This class should be the only class in this file
class version(str):
    @classmethod
    def __new__(cls, *args, **kwargs):
        obj = super(version, cls).__new__(*args)

        var_name = kwargs.get('var_name', None)
        if not var_name:
            var_name = cls.__name__

        module = _get_caller_module(1)
        module.__dict__[var_name] = obj

        return obj
