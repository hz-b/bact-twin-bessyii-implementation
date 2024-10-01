from typing import Tuple

from bact_twin_architecture.interfaces.id_property_transformer import (
    IdentifierPropertyTransformerBase,
)
from bact_twin_architecture.interfaces.identifier import DeviceIdentifier


class IdentifierPropertyTransformer(IdentifierPropertyTransformerBase):
    """I guess that will not be that simple

    Todo:
        implement it properly!
        Should map id, property to id, property

        Define interface class for it
    """

    def forward(self, id: str, property: str) -> Tuple[DeviceIdentifier, str]:
        if property == "x_kick":
            return "current"
        elif property == "y_kick":
            return "current"
        else:
            raise NotImplementedError(f"not handling {property}. I am a hack anyway")

    def inverse(self, id, property):
        raise NotImplementedError(f"not handling {property}. I am a hack anyway")
