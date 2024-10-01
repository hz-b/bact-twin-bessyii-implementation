import json
from bact_twin_architecture.data_model.command import Command, CommandSequence
from bact_twin_bessyii_impl.bl.bluesky_measurement_execution_engine import BlueskyMeasurementExecutionEngine
from bact_twin_bessyii_impl.bl.io.pytac_repositories import PyTACRepository
from bact_twin_bessyii_impl.bl.state_conversion import UnitConversionRepo, UnitConversionFacade
from ophyd import Component as Cpt, Device, DynamicDeviceComponent, EpicsSignal, EpicsSignalRO, PVPositionerPC
from bluesky.run_engine import RunEngine

repo = PyTACRepository()

class SteererCurrent(PVPositionerPC):
    setpoint = Cpt(EpicsSignal, ":set")
    readback = Cpt(EpicsSignalRO, ":set")


class Steerer(Device):
    current = Cpt(SteererCurrent, "", name="cur")


with open("orm_commands.json") as fp:
    tmp = json.load(fp)
cmds_on_lattice = CommandSequence(commands=[Command(**d) for d in tmp["commands"]])
transformer = UnitConversionFacade(
    UnitConversionRepo(conversion_info=tuple(repo.state_conversion_repo))
)
cmds_on_machine = CommandSequence(commands=[
    transformer.command_rewrite_forward(cmd) for cmd in cmds_on_lattice.commands
])
cmds_on_machine
device_ids = set([cmd.id for cmd in cmds_on_machine.commands])

class SteererCollection:
    steerers = DynamicDeviceComponent(device_ids)
    pass

# RE = bluesky.run_engine.RunEngine()
# mexec = BlueskyMeasurementExecutionEngine(run_engine=RE, devices=)
