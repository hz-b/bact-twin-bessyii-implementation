from typing import Sequence, Dict

from bact_twin_architecture.data_model.command import Command
from bact_twin_architecture.interfaces.measurement_execution_engine import MeasurementExecutionEngine
import bluesky.plan_stubs as bps


def commands_as_messages(devices, commands : Sequence[Command]):
    """
        Implement stop, ignore, rollback etc
    """
    for command in commands:
        # first select the device
        t_device = devices[command.id]
        signal = getattr(t_device, command.property)
        # Do I need some way to translate this
        # command
        yield from bps.mv(signal, command.value)
        # read all devices
        yield from bps.trigger_and_read(devices)


def commands_execution_plan(devices, commands: Sequence[Command]):
    """
    Todo:
        Wrap it to a plan
    """
    r = yield from commands_as_messages(devices, commands)
    return r


class BlueskyMeasurementExecutionEngine(MeasurementExecutionEngine):
    def __init__(self, run_engine: bluesky.RunEngine, devices : Dict[object]):
        """

        Todo:
            Specify the device type
        """
        self.run_engine = run_engine
        self.devices = devices

    def execute(self, commands:  Sequence[Command]) -> str:
        uid, = self.run_engine(self.devices, commands_execution_plan(commands))
        return uid