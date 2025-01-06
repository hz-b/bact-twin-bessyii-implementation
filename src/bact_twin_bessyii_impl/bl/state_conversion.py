"""convert from lattice element change to device property

Please note:
    here we have to map (lattice_name, property) -> (device_name, property)

Todo:
   Split up content in different modules
"""

from typing import Union

from bact_twin_architecture.data_model.command import Command
from bact_twin_architecture.data_model.identifiers import (
    LatticeElementPropertyID,
    DevicePropertyID, ConversionID,
)
from bact_twin_architecture.interfaces.command_rewritter import CommandRewriterBase
from bact_twin_architecture.interfaces.translator_service import TranslatorServiceBase
from bact_twin_architecture.utils.unit_conversion import (
    UnitConversion,
    LinearUnitConversion,
)

from bact_twin_bessyii_impl.bl.liaison_manager import  LiaisonManager


class CommandRewriter(CommandRewriterBase):
    """
    Todo:
        split it up in different objects?
        seems to have more than one responsibility

        Move it to bact_twin_architecture.utils?
    """

    def __init__(self, translation_service: TranslatorServiceBase):
        """create the factory based on the repo that reads in the pytac files"""
        self.translator_service = translation_service
        self.liaison_manager = LiaisonManager()


    def backward(self, cmd: Command) -> Command:
        """
        Todo:
            just take it out and make it a function?
        """
        lat_prop_id = LatticeElementPropertyID(
            element_name=cmd.id, property=cmd.property
        )
        dev_prop_id = self.liaison_manager.forward(lat_prop_id)
        translation_object = self.translator_service.get(
            ConversionID(lattice_property_id=lat_prop_id, device_property_id=dev_prop_id)
        )

        assert dev_prop_id.device_name is not None

        ncmd = Command(
            id=dev_prop_id.device_name,
            property=dev_prop_id.property,
            value=translation_object.forward(cmd.value),
            behaviour_on_error=cmd.behaviour_on_error,
        )
        return ncmd

    def forward(self, cmd: Command) -> Command:
        """
        Todo:
            just take it out and make it a function?
        """
        lat_prop_id = LatticeElementPropertyID(
            element_name=cmd.id, property=cmd.property
        )
        dev_prop_id = self.liaison_manager.forward(lat_prop_id)
        translation_object = self.translator_service.get(
            ConversionID(lattice_property_id=lat_prop_id, device_property_id=dev_prop_id)
        )

        assert dev_prop_id.device_name is not None

        ncmd = Command(
            id=dev_prop_id.device_name,
            property=dev_prop_id.property,
            value=translation_object.forward(cmd.value),
            behaviour_on_error=cmd.behaviour_on_error,
        )
        return ncmd

