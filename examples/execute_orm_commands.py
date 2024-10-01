import json
from bact_twin_architecture.data_model.command import Command, CommandSequence
from bact_twin_bessyii_impl.bl.bluesky_measurement_execution_engine import BlueskyMeasurementExecutionEngine
from bact_twin_bessyii_impl.bl.io.pytac_repositories import PyTACRepository
from bact_twin_bessyii_impl.bl.state_conversion import UnitConversionRepo, UnitConversionFacade
from ophyd import Component as Cpt, EpicsSignal, EpicsSignalRO, PVPositionerPC
from bluesky.run_engine import RunEngine

repo = PyTACRepository()


class Steerer(PVPositionerPC):
    setpoint = Cpt(EpicsSignal, ":set")
    readback = Cpt(EpicsSignalRO, ":set")


with open("orm_commands.json") as fp:
    tmp = json.load(fp)
cmds_on_lattice = CommandSequence(commands=[Command(**d) for d in tmp["commands"]])
transformer = UnitConversionFacade(
    UnitConversionRepo(conversion_info=tuple(repo.state_conversion_repo))
)
cmds_on_machine = CommandSequence(commands=[
    transformer.command_rewrite_forward(cmd) for cmd in cmds_on_lattice.commands
])
# RE = bluesky.run_engine.RunEngine()
# mexec = BlueskyMeasurementExecutionEngine(run_engine=RE, devices=)
