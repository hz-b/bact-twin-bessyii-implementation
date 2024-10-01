"""convert from lattice element change to device property

Please note:
    here we have to map (lattice_name, property) -> (device_name, property)
"""
import functools
from dataclasses import dataclass
from typing import Sequence, Tuple

from bact_twin_architecture.data_model.command import Command
from bact_twin_architecture.interfaces.identifier import Identifier
from bact_twin_architecture.interfaces.state_conversion import StateConversion

from bact_twin_bessyii_impl.bl.io.pytac_repositories import LinearUnitConversionInfo


class UnitConversion(StateConversion):
    """a one dimensional conversion
    """


class LinearUnitConversion(UnitConversion):
    """

    Warning:
        inverse will fail for slopes of 0
    """
    def __init__(self, *, intercept: float, slope: float):
        self.intercept  = intercept
        self.slope = slope

    def forward(self, state: float) -> float:
        return self.intercept + self.slope  * state

    def inverse(self, state: float) -> float:
        return (state - self.intercept) / self.slope


@dataclass(frozen=True)
class UnitConversionRepo:
    conversion_info: Tuple[LinearUnitConversionInfo]

    def _lookup_table_create(self):
        return {
            (item.position_name, item.property): item
            for item in self.conversion_info
            if item.position_name is not None and item.property is not None
        }

    @functools.lru_cache(maxsize=1)
    def _lookup_table(self):
        r  = self._lookup_table_create()
        return r

    def get(self, pos_name: str, property: str):
        lut =  self._lookup_table()
        obj =  lut[(pos_name, property)]
        return obj

class UnitConversionFacade:
    def __init__(self, unit_conversion_repo : UnitConversionRepo):
        """create the factory based on the repo that reads in the pytac files
        """
        self.unit_conversion_repo = unit_conversion_repo

    def get(self, id: Identifier, property: str) -> UnitConversion:
        """
        Todo:
            revisit to be far more flexible: not only linear conversion
        """
        linear = self.unit_conversion_repo.get(id, property)
        return LinearUnitConversion(slope=linear.slope, intercept=linear.intercept)

    def update_forward(self, id: Identifier, property: str, value: float) -> float:
        """
        Todo:
            Need to distinquish ...
            id: lattice identifer or device identifier
            Please note, often the same names are used for the lattice
            identifier and the device identifier

            These then start to mix
        """
        return self.get(id, property).forward(value)

    def update_inverse(self, id: Identifier, property: str, value: float) -> float:
        return self.get(id, property).inverse(value)



    def command_rewrite_forward(self, cmd : Command) -> Command:
        return Command(
            id=cmd.id,
            property=cmd.property,
            value=self.update_forward(cmd.id, cmd.property, cmd.value),
            behaviour_on_error=cmd.behaviour_on_error
        )
