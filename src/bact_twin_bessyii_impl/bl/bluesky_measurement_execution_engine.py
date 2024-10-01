"""Demonstrator of a measurement execution engine

Todo:
    * implement full functionality

Missing features:

* handling behaviour_on_error
* how much of the accelerator access to wrap?
* hide devices behind a software multiplexer?
  In its current form quite some information will be stored
  in the databroker

"""
from typing import Sequence, Dict

from bact_twin_architecture.data_model.command import Command
from bact_twin_architecture.interfaces.measurement_execution_engine import (
    MeasurementExecutionEngine,
)
import bluesky.preprocessors as bpp
import bluesky.plan_stubs as bps
from bluesky import RunEngine

from ophyd import Device, Signal


def commands_plan(
    commands: Sequence[Command],
    detectors: Sequence[Device],
    actuators: Dict[str, Device],
    info_signals: Dict[str, Signal],
):
    """

    Inner plan for :func:`commands_execution_plan`

    Todo:
        Implement stop, ignore, rollback etc
        Device replace by ophyd_async.Settable
        info_signals as dataclass?
    """
    all_dev = list(info_signals.values()) + list(detectors) + list(actuators.values())
    dev_name = info_signals["device_name"]
    ch_name = info_signals["channel_name"]
    ch_val = info_signals["channel_value"]
    for command in commands:
        # first select the device
        t_device = actuators[command.id]
        channel = getattr(t_device, command.property)
        # then apply it to all
        yield from bps.mv(
            dev_name,
            str(command.id),
            ch_name,
            str(command.property),
            ch_val,
            command.value,
            channel,
            command.value,
        )
        # read all devices
        yield from bps.trigger_and_read(all_dev)


def commands_execution_plan(
    commands: Sequence[Command],
    detectors: Sequence[Device],
    actuators: Dict[str, Device],
    info_signals: Dict[str, Signal],
    md: None,
):
    """Translate commands to bluesky run-engine messages"""
    _md = md or dict()
    _md.update(dict(commands=commands))

    @bpp.stage_decorator(list(detectors) + list(actuators.values()))
    @bpp.run_decorator(md=_md)
    def inner():
        r = yield from commands_plan(
            commands=commands,
            detectors=detectors,
            actuators=actuators,
            info_signals=info_signals,
        )
        return r

    r = yield from inner()
    return r


class BlueskyMeasurementExecutionEngine(MeasurementExecutionEngine):
    """Demonstrator of a measurement engine as a bluesky runengine"""

    def __init__(self, run_engine: RunEngine):
        """

        Todo:
            Specify the device type
        """
        self.run_engine = run_engine

    def execute(
        self,
        commands: Sequence[Command],
        detectors: Sequence[Device],
        actuators: Dict[str, Device],
        info_signals: Dict[str, Signal],
        md: Dict[str, object] = None,
    ) -> str:
        plan = commands_execution_plan(
            commands=commands,
            detectors=detectors,
            actuators=actuators,
            info_signals=info_signals,
            md=md,
        )
        (uid,) = self.run_engine(plan)
        return uid
