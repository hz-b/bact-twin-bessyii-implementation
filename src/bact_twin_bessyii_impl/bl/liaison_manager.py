from typing import Mapping, Sequence
import logging

from bact_twin_architecture.data_model.identifiers import  DevicePropertyID, LatticeElementPropertyID
from bact_twin_architecture.interfaces.liaison_manager import LiaisonManagerBase

logger = logging.getLogger("bact-twin-bessyii-impl")


class LiaisonManager(LiaisonManagerBase):
    def __init__(
        self,
        forward_lut: Mapping[LatticeElementPropertyID, Sequence[DevicePropertyID]],
        inverse_lut: Mapping[DevicePropertyID, Sequence[LatticeElementPropertyID]],
    ):
        self.forward_lut = forward_lut
        self.inverse_lut = inverse_lut

    def forward(self, id_: LatticeElementPropertyID) -> Sequence[DevicePropertyID]:
        try:
            return self.forward_lut[id_]
        except KeyError as ke:
            logger.error(
                f"{self.__class__.__name__} I did not find id {id_} in lookup table: {ke}"
            )
            raise ke

    def inverse(self, id_: DevicePropertyID) -> Sequence[LatticeElementPropertyID]:
        try:
            return self.inverse_lut[id_]
        except KeyError as ke:
            logger.error(
                f"{self.__class__.__name__} I did not find id {id_} in lookup table: {ke}"
            )
            raise ke
