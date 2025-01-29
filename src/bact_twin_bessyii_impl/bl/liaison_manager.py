from multiprocessing.managers import Value

from bact_twin_architecture.data_model.identifiers import DevicePropertyID, LatticeElementPropertyID
from bact_twin_architecture.interfaces.liaison_manager import (
    LiaisonManagerBase,
)


class LiaisonManager(LiaisonManagerBase):
    """I guess that will not be that simple

    Todo:
        implement it properly!
        Should map id, property to id, property

        Define interface class for it

    This liasion manager will get much simpler with yellow pages at hand

    Then I need only to ask yellow pages if the id belongs to some family
    """

    def forward(self, id_: LatticeElementPropertyID) -> DevicePropertyID:
        if id_.property == "x_kick":
            return DevicePropertyID(device_name="H" + id_.element_name, property="current")
        elif id_.property == "y_kick":
            return DevicePropertyID(device_name="V"+id_.element_name, property="current")
        else:
            raise NotImplementedError(f"not handling {property}. I am a hack anyway")

    def inverse(self, id_ : DevicePropertyID) -> LatticeElementPropertyID:
        if id_.property in ("x", "y"):
            return LatticeElementPropertyID(element_name=id_.device_name, property=id_.property)

        if self._check_if_steerer_name(id_.device_name):
            return self.steerer_power_converter_to_steerer_magnet(id_)

        raise NotImplementedError(f"not handling {property}. I am a hack anyway")

    def steerer_power_converter_to_steerer_magnet(self, id_: DevicePropertyID) -> LatticeElementPropertyID:
        """a very BESSY II specific hack

        assumes that name is checked
        """
        assert self._check_if_steerer_name(id_.device_name)
        assert id_.property == "set_current"


        # at BESSYII they are mounted on sextupoles
        magnet_name = id_.device_name[1:]
        magnet_name = magnet_name.replace("P", "M")
        if self._check_if_horizontal_steerer_name(id_.device_name):
            return LatticeElementPropertyID(element_name=magnet_name, property="x_kick")
        elif self._check_if_vertical_steerer_name(id_.device_name):
            return LatticeElementPropertyID(element_name=magnet_name, property="y_kick")
        else:
            raise ValueError("should not end up here")

    def _check_if_steerer_name(self, name):
        return (
            self._check_if_horizontal_steerer_name(name)
            or self._check_if_vertical_steerer_name(name)
        )

    def _check_if_horizontal_steerer_name(self, name: str) -> bool:
        return self._check_steerer_common_pattern(name) and name[0] == "H"

    def _check_if_vertical_steerer_name(self, name: str) -> bool:
        return self._check_steerer_common_pattern(name) and name[0] == "V"

    def _check_steerer_common_pattern(self, name: str) -> bool:
        if name[1] != "S":
            return False

        if name[2] == "P":
            return name[3] in ("1", "2")

        elif name[2] in ("1", "2", "3", "4"):
            return True
        else:
            return False
