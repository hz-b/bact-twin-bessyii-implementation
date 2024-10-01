"""convert from lattice element change to device property

Please note:
    here we have to map (lattice_name, property) -> (device_name, property)
"""
from bact_twin_architecture.interfaces.identifier import Identifier
from bact_twin_architecture.interfaces.state_conversion import StateConversion


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


class UnitConversionFacade:
    def __init__(self):
        # To sielence syntax check
        self.db = dict()
        raise NotImplementedError

    def get(self, id: Identifier, property: str) -> UnitConversion:
        return self.db[id][property]

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


class PyTACUnitConversionFacade(UnitConversionFacade):
    def __int__(self, db):
        """create the factory based on the repo that reads in the pytac files
        """

