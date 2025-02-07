from typing import Sequence

from bact_twin_architecture.data_model.identifiers import (
    DevicePropertyID,
    LatticeElementPropertyID,
)
from bact_twin_architecture.interfaces.liaison_manager import (
    LiaisonManagerBase,
)

from .bessyii_nomen_clature import (
    name_matches_steerer_name,
    name_matches_horizontal_steerer_name,
    name_matches_vertical_steerer_name,
)


class LiaisonManager(LiaisonManagerBase):
    """I guess that will not be that simple

    Todo:
        implement it properly!
        Should map id, property to id, property

        Use Waheeds data constant

    This liasion manager will get much simpler with yellow pages at hand

    Then I need only to ask yellow pages if the id belongs to some family
    """

    def forward(self, id_: LatticeElementPropertyID) -> Sequence[DevicePropertyID]:
        if id_.property == "x_kick":
            return (
                DevicePropertyID(
                    device_name="H" + id_.element_name, property="current"
                ),
            )
        elif id_.property == "y_kick":
            return (
                DevicePropertyID(
                    device_name="V" + id_.element_name, property="current"
                ),
            )
        else:
            raise NotImplementedError(f"not handling {property}. I am a hack anyway")

    def inverse(self, id_: DevicePropertyID) -> Sequence[LatticeElementPropertyID]:
        if id_.property in ("x", "y", "K"):
            # idem potent type
            return [
                LatticeElementPropertyID(
                    element_name=id_.device_name, property=id_.property
                )
            ]

        elif self._check_if_steerer_name(id_.device_name):
            return [self.steerer_power_converter_to_steerer_magnet(id_)]
        elif self._check_if_master_clock_name(id_.device_name):
            return self.master_clock_to_cavities(id_)

        raise NotImplementedError(f"not handling {property}. I am a hack anyway")

    def master_clock_to_cavities(
        self, id_: DevicePropertyID
    ) -> Sequence[LatticeElementPropertyID]:
        assert self._check_if_master_clock_name(id_.device_name)
        if id_.property != "reference_frequency":
            raise AssertionError(
                f"{self.__class__.__name__}: for master clock I am handling only frequency now"
            )

        cavity_names = ["CAVH4T8R", "CAVH3T8R", "CAVH2T8R", "CAVH1T8R"]
        return [
            LatticeElementPropertyID(element_name=name, property="frequency")
            for name in cavity_names
        ]

    def steerer_power_converter_to_steerer_magnet(
        self, id_: DevicePropertyID
    ) -> LatticeElementPropertyID:
        """a very BESSY II specific hack

        assumes that name is checked
        """
        assert name_matches_steerer_name(id_.device_name)
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

    def _check_if_master_clock_name(self, name):
        return name in ["MCLKHX251C"]

    def _check_if_steerer_name(self, name):
        return name_matches_steerer_name(name)

    def _check_if_horizontal_steerer_name(self, name: str) -> bool:
        return name_matches_horizontal_steerer_name(name)

    def _check_if_vertical_steerer_name(self, name: str) -> bool:
        return name_matches_vertical_steerer_name(name)
