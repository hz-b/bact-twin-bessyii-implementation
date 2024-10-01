from bact_twin_architecture.data_model.identifiers import DevicePropertyID, LatticeElementPropertyID
from bact_twin_architecture.interfaces.id_property_transformer import (
    IdentifierPropertyTransformerBase,
)


class IdentifierPropertyTransformer(IdentifierPropertyTransformerBase):
    """I guess that will not be that simple

    Todo:
        implement it properly!
        Should map id, property to id, property

        Define interface class for it
    """

    def forward(self, id_: LatticeElementPropertyID) -> DevicePropertyID:
        if id_.property == "x_kick":
            return DevicePropertyID(device_name=None, property="current")
        elif id_.property == "y_kick":
            return DevicePropertyID(device_name=None, property="current")
        else:
            raise NotImplementedError(f"not handling {property}. I am a hack anyway")

    def inverse(self, id_ : DevicePropertyID) -> LatticeElementPropertyID:
        raise NotImplementedError(f"not handling {property}. I am a hack anyway")
