from abc import ABCMeta, abstractmethod


class Extension(object):
    """
    Abstract class for implementing extensions to Pylease. The minimal
    implementation should override the execute method. That method will be
    supplied with the arguments from the command line.
    """
    __metaclass__ = ABCMeta

    def __init__(self, arg_parser):
        super(Extension, self).__init__()

        self.arg_parser = arg_parser

    @abstractmethod
    def execute(self, args, version):
        pass

    @classmethod
    def init_all(cls, extensions, arg_parser):
        """
        Initialize all extension provided as the extensions list

        :param extensions: The list of Extension class implementations
        :param arg_parser: The argument parser
        :return: List of Extension objects
        """
        result = []

        for extension in extensions:
            result.append(extension(arg_parser))

        return result

    @classmethod
    def execute_all(cls, extensions, args, version):
        """
        Calls execute method on all Extension objects provided as the
        extensions list.

        :param extensions: List of Extension objects
        :param args: Command-line arguments, will be supplied to Extension
                     objects' execute method.
        :param version: The version being released
        """
        for extension in extensions:
            extension.execute(args, version)
