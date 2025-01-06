from typing import Sequence

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


class Steerer(Device):
    """Steerer power converter with current

    Real steerers will have extra signals: e.g. state
    Typically the states  would be checked during
    staging the devices: e.g. to detect early that a
    power converter is off etc.
    """

    current = Cpt(SteererCurrent, "", name="cur")


def setup(device_ids: Sequence[str]):
    """
    Todo:  retrieve steerer names from some service
    """
    class SteererCollection(Device):
        """ """

        col = DynamicDeviceComponent(
            {
                dev_name: (Steerer, dev_name, dict(lazy=True))
                for dev_name in device_ids
            },
        )

    steerers = SteererCollection("Pierre:DT:", name="st_col")
    bpms = BPM("Pierre:DT:MDIZ2T5G", name="bpm")
    if not bpms.connected:
        bpms.wait_for_connection()
    return bpms, steerers


__all__ = ["Steerer", "SteererCurrent"]