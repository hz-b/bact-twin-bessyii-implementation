"""convert from lattice element change to device property

Please note:
    here we have to map (lattice_name, property) -> (device_name, property)

Todo:
   Split up content in different modules
"""

from typing import Tuple, Union

from bact_twin_architecture.data_model.command import Command
from bact_twin_architecture.data_model.identifiers import (
    LatticeElementPropertyID,
    DevicePropertyID,
)
from bact_twin_architecture.data_model.unit_conversion_repo import UnitConversionRepo
from bact_twin_architecture.data_model.unit_conversion_info import (
    LinearUnitConversionInfo,
)
from bact_twin_architecture.utils.unit_conversion import (
    UnitConversion,
    LinearUnitConversion,
)

from bact_twin_bessyii_impl.bl.element_property_tranformer import (
    IdentifierPropertyTransformer,
)


class UnitConversionFacade:
    """
    Todo:
        split it up in different objects?
        seems to have more than one responsibility
    """

    def __init__(self, unit_conversion_repo: UnitConversionRepo):
        """create the factory based on the repo that reads in the pytac files"""
        self.unit_conversion_repo = unit_conversion_repo
        self.property_renamer = IdentifierPropertyTransformer()

    def get_conversion_info(
        self, id_: Union[LatticeElementPropertyID, DevicePropertyID]
    ) -> LinearUnitConversionInfo:
        return self.unit_conversion_repo.get(id_)

    def get_converter(
        self, id_: Union[LatticeElementPropertyID, DevicePropertyID]
    ) -> UnitConversion:
        """
        Todo:
            revisit to be far more flexible: not only linear conversion
        """
        linear = self.unit_conversion_repo.get(id_)
        return LinearUnitConversion(slope=linear.slope, intercept=linear.intercept)

    def update_forward(self, id_: LatticeElementPropertyID, value: float) -> float:
        """
        Todo:
            Need to distinquish ...
            id: lattice identifer or device identifier
            Please note, often the same names are used for the lattice
            identifier and the device identifier

            These then start to mix
        """
        return self.get_converter(id_).forward(value)

    def update_inverse(self, id_: DevicePropertyID, value: float) -> float:
        return self.get_converter(id_).inverse(value)

    def command_rewrite_forward(self, cmd: Command) -> Command:
        """
        Todo:
            just take it out and make it a function?
        """
        lat_prop_id = LatticeElementPropertyID(
            element_name=cmd.id, property=cmd.property
        )
        dev_prop_id = self.property_renamer.forward(lat_prop_id)
        # Todo: fix this hack ... this info should be part of the renamer
        info = self.get_conversion_info(lat_prop_id)
        dev_name = info.conversion_id.device_property_id.device_name

        assert dev_name is not None
        ncmd = Command(
            id=dev_name,
            property=dev_prop_id.property,
            value=self.update_forward(id_=lat_prop_id, value=cmd.value),
            behaviour_on_error=cmd.behaviour_on_error,
        )
        return ncmd
