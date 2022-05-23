# IMPORTS ------

from typing import Protocol

# PROTOCOL ------
"""
DOC
"""


class sensor(Protocol):
    def give_measure_info():
        ...

    def give_place_info():
        ...

    def give_sensor_info():
        ...
