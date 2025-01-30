"""convert from lattice element change to device property

Please note:
    here we have to map (lattice_name, property) -> (device_name, property)

Todo:
   Split up content in different modules
"""

from typing import Union, Sequence

from bact_twin_architecture.data_model.command import Command
from bact_twin_architecture.data_model.identifiers import (
    LatticeElementPropertyID,
    DevicePropertyID, ConversionID,
)
from bact_twin_architecture.interfaces.command_rewritter import CommandRewriterBase
from bact_twin_architecture.interfaces.liaison_manager import LiaisonManagerBase
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

    def __init__(self, liasion_manager: LiaisonManagerBase, translation_service: TranslatorServiceBase):
        """create the factory based on the repo that reads in the pytac files"""
        self.translator_service = translation_service
        self.liaison_manager = liasion_manager

    def inverse(self, cmd: Command) -> Sequence[Command]:
        """
        Todo:
            just take it out and make it a function?
        """
        dev_prop_id = DevicePropertyID(
            device_name=cmd.id, property=cmd.property
        )
        lat_prop_ids = self.liaison_manager.inverse(dev_prop_id)

        return [self.inverse_translate_one(cmd, dev_prop_id, lat_prop_id) for lat_prop_id in lat_prop_ids]

    def inverse_translate_one(self, cmd: Command, dev_prop_id: DevicePropertyID,
                                  lat_prop_id: LatticeElementPropertyID) -> Command:

        translation_object = self.translator_service.get(
            ConversionID(lattice_property_id=lat_prop_id, device_property_id=dev_prop_id)
        )

        assert dev_prop_id.device_name is not None

        ncmd = Command(
            id=lat_prop_id.element_name,
            property=lat_prop_id.property,
            value=translation_object.inverse(cmd.value),
            behaviour_on_error=cmd.behaviour_on_error,
        )
        return ncmd

    def forward(self, cmd: Command) -> Sequence[Command]:
        """
        Todo:
            just take it out and make it a function?
        """
        lat_prop_id = LatticeElementPropertyID(
            element_name=cmd.id, property=cmd.property
        )
        dev_prop_ids = self.liaison_manager.forward(lat_prop_id)
        return [self.forward_translate_one(cmd, lat_prop_id, dev_prop_id) for dev_prop_id in dev_prop_ids]

    def forward_translate_one(self, cmd: Command,
        lat_prop_id: LatticeElementPropertyID,
        dev_prop_id: DevicePropertyID,
    ) -> Command:
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

