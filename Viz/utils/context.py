import json

from Viz.pesudo_algorithms import algorithmExporter


class Singleton(type):
    """
    Meta class to create a singleton type
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Context(metaclass=Singleton):
    """
    Singleton class to represent the context that can be passed to the Django templating language
    """

    def __init__(self):
        self.__context: dict = dict()
        self.__context["primaryColour"] = "#e57373 red lighten-2"
        self.__context["secondaryColour"] = "#7986cb indigo lighten-2"
        self.__context["primaryText"] = "#black-text"
        self.__context["pageTitle"] = "A Title"

    def getContext(self) -> dict:
        """
        Returns a context
        :return: context as a dict
        """
        # make object imputable
        return dict(**self.__context)
