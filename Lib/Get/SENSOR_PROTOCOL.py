# IMPORTS ------

from typing import Protocol

import pandas as pd

# PROTOCOL ------
"""
DOC
"""


class sensor(Protocol):
    def give_measure_info(self) -> pd.DataFrame:
        ...

    def give_place_info(self) -> dict:
        ...

    def give_sensor_info(self) -> dict:
        ...

    def give_meta_info(self) -> dict:
        ...
