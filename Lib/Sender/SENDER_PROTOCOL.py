# IMPORTS ------

from typing import Protocol


class Injector(Protocol):
    """
    DOC
    """

    def create_sensor(self):
        ...

    def create_place(self):
        ...

    def injection(self):
        ...
