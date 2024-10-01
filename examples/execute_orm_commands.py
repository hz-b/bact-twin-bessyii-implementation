"""Demonstrator of using bluesky run engine as measurement executor

Todo:
   * Split up functionality.
   * Review how dynamically the required accelerator devices should
     be created.
   * Should a software multiplexer handle access to all the devices
     that are required for wrapping an accelerator

Here the steerers are created with devices of minimal functionallity.
Proper devices would use bluesky's synchronisation abilities.

"""
from bact_twin_architecture.data_model.command import Command, CommandSequence
from bact_twin_bessyii_impl.bl.bluesky_measurement_execution_engine import (
    BlueskyMeasurementExecutionEngine,
)
from bact_twin_bessyii_impl.bl.io.pytac_repositories import PyTACRepository
from bact_twin_bessyii_impl.bl.state_conversion import (
    UnitConversionRepo,
    UnitConversionFacade,
)
from ophyd import (
    Component as Cpt,
    Device,
    DynamicDeviceComponent,
    EpicsSignal,
    EpicsSignalRO,
    PVPositionerPC,
    Signal,
)
from bluesky.run_engine import RunEngine
import bluesky.plans as bp
from bluesky.callbacks import LiveTable
import json


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


# use data stored in pytac data csv files to crate
# required repositories
repo = PyTACRepository()
transformer = UnitConversionFacade(
    UnitConversionRepo(conversion_info=tuple(repo.state_conversion_repo))
)
# load the commands that operate in lattice space and transform
# them to machine state
with open("orm_commands.json") as fp:
    tmp = json.load(fp)
cmds_on_lattice = CommandSequence(commands=[Command(**d) for d in tmp["commands"]])
cmds_on_machine = CommandSequence(
    commands=[
        transformer.command_rewrite_forward(cmd) for cmd in cmds_on_lattice.commands
    ]
)

# dynamically create the steerer devices that are actually required
# for a whole accelerator it would be a bit more complex
# again review if here a software multiplexer would not be closer
# to the task
device_ids = set([cmd.id for cmd in cmds_on_machine.commands])


class SteererCollection(Device):
    """ """

    col = DynamicDeviceComponent(
        {
            dev_name: (Steerer, "Anonym:DT:" + dev_name, dict(lazy=True))
            for dev_name in device_ids
        },
    )


steerers = SteererCollection(name="st_col")
actuators = {name: getattr(steerers.col, name) for name in steerers.col.component_names}
# used so that it is easier to see what is happening
# could be included in the standard software multiplexer
info_sigs = {
    name: Signal(name=name) for name in ["device_name", "channel_name", "channel_value"]
}
lt = LiveTable(
    list([sig.name for _, sig in info_sigs.items()]),  # + list(actuators.values())
    default_prec=10,
)
RE = RunEngine()
# here a databroker should be added so that data can be accessed
# later on
RE.subscribe(lt)

md = dict(commands_on_lattice=cmds_on_lattice)
mexec = BlueskyMeasurementExecutionEngine(run_engine=RE)
mexec.execute(
    commands=cmds_on_machine.commands,
    # need to add bpms
    detectors=[],
    actuators=actuators,
    info_signals=info_sigs,
    md=md,
)
