SELECTED_NODE_COLOR = "#f44336"
CURRENT_NODE_COLOR = "#ffeb3b"
NEIGHBOUR_NODE_COLOR = "#ce93d8"

SELECTED_NODE_COLOR_HTML = "red lighten-2"
CURRENT_NODE_COLOR_HTML = "yellow lighten-1"
NEIGHBOUR_NODE_COLOR_HTML = "purple lighten-3"

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
        self.__context["primaryColour"] = "#e57373 grey lighten-5"
        self.__context["secondaryColour"] = "#eeeeee grey lighten-3"
        self.__context["buttonColour"] = "purple lighten-1"
        self.__context["primaryText"] = "#black-text"
        self.__context["pageTitle"] = "A Title"
        self.__context["selectedNodeColor"] = SELECTED_NODE_COLOR
        self.__context["currentNodeColor"] = CURRENT_NODE_COLOR
        self.__context["neighbourNodeColor"] = NEIGHBOUR_NODE_COLOR
        self.__context["isSourceNeeded"] = True

    def getContext(self) -> dict:
        """
        Returns a context
        :return: context as a dict
        """
        # make object imputable
        return dict(**self.__context)
