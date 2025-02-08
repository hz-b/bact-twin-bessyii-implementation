from typing import Sequence, List

from ophyd import (
    Component as Cpt,
    Device,
    DynamicDeviceComponent,
    EpicsSignal,
    EpicsSignalRO,
    PVPositionerPC,
    Signal,
)
# currently in an other package: could be distributed here too
from bact_bessyii_ophyd.devices.pp.bpm.bpm import BPM


class SteererCurrent(PVPositionerPC):
    """simplest devices

    Warning:
       Does not check if setpoint and readback are in
       range
    """

    setpoint = Cpt(EpicsSignal, ":set")
    readback = Cpt(EpicsSignalRO, ":set")


class SteererDeltaCurrent(Device):
    def set(self, diff_value):
        value = self.parent.set_current_at_start.get() + diff_value
        return self.parent.current.set(value)


class Steerer(Device):
    """Steerer power converter with current

    Real steerers will have extra signals: e.g. state
    Typically the states  would be checked during
    staging the devices: e.g. to detect early that a
    power converter is off etc.
    """

    current = Cpt(SteererCurrent, "", name="cur")
    delta_set_current = Cpt(SteererDeltaCurrent, suffix="", name="delta_cur")
    set_current_at_start = Cpt(Signal,  name="at_start")

    def stage(self) -> List[object]:
        r = super().stage()
        self.set_current_at_start.put(self.current.setpoint.get())
        return r

    def unstage(self) -> List[object]:
        """

        Todo:
            shall one reset the value to the start current?
        """
        return super().unstage()


def setup(device_ids: Sequence[str], prefix="Anonym:"):
    """
    Todo:  retrieve steerer names from some service
    """
    class SteererCollection(Device):
        """ """

        col = DynamicDeviceComponent(
            {
                dev_name: (Steerer, dev_name, dict(lazy=False))
                for dev_name in device_ids
            },
        )

    steerers = SteererCollection(prefix, name="st_col")
    bpms = BPM(f"{prefix}MDIZ2T5G", name="bpm")
    if not bpms.connected:
        bpms.wait_for_connection()
    if not steerers.connected:
        steerers.wait_for_connection(timeout=5)
    for name in steerers.col.component_names:
        st = getattr(steerers.col, name)
        if not st.connected:
            steerers.wait_for_connection(timeout=5)

    return bpms, steerers


__all__ = ["Steerer", "SteererCurrent"]