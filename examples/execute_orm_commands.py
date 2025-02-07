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
from dataclasses import asdict

from bact_twin_architecture.data_model.command import Command, CommandSequence
from ophyd import Signal

from bact_twin_bessyii_impl.bl.bessyii_bluesky_me import setup
from bact_twin_bessyii_impl.bl.bluesky_measurement_execution_engine import (
    BlueskyMeasurementExecutionEngine,
)
from bact_twin_bessyii_impl.bl.command_rewritter import CommandRewriter
from bact_twin_bessyii_impl.bl.io.pytac_repositories import PyTACRepository


from bluesky.run_engine import RunEngine
from bluesky.callbacks import LiveTable
from databroker import catalog
import json

from bact_twin_bessyii_impl.bl.translation_service import TranslationService

# use data stored in pytac data csv files to crate
# required repositories
repo = PyTACRepository()

transformer = CommandRewriter(TranslationService(conversion_info=repo.state_conversion_repo))
# load the commands that operate in lattice space and transform
# them to machine state
with open("orm_commands.json") as fp:
    tmp = json.load(fp)
cmds_on_lattice = CommandSequence(commands=[Command(**d) for d in tmp["commands"]])
cmds_on_machine = CommandSequence(
    commands=[
        transformer.forward(cmd) for cmd in cmds_on_lattice.commands
    ]
)

# dynamically create the steerer devices that are actually required
# for a whole accelerator it would be a bit more complex
# again review if here a software multiplexer would not be closer
# to the task
device_ids = set([cmd.id for cmd in cmds_on_machine.commands])

bpms, steerers = setup(device_ids=tuple(device_ids))

print(f"{bpms.count.name=}")

actuators = {name: getattr(steerers.col, name) for name in steerers.col.component_names}
# used so that it is easier to see what is happening
# could be included in the standard software multiplexer
info_sigs = {
    name: Signal(name=name) for name in ["device_name", "channel_name", "channel_value"]
}
lt = LiveTable(
    [sig.name for _, sig in info_sigs.items()] + [bpms.count.name],  # + list(actuators.values())
    default_prec=10,
)
RE = RunEngine()
# here a databroker should be added so that data can be accessed
# later on
RE.subscribe(lt)
db = catalog["heavy_local"]
RE.subscribe(db.v1.insert)

# mongodb can not store the command object ?
md = dict(commands_on_lattice=[asdict(cmd) for cmd in cmds_on_lattice.commands])
mexec = BlueskyMeasurementExecutionEngine(run_engine=RE)
mexec.execute(
    commands=cmds_on_machine.commands,
    # need to add bpms
    detectors=[bpms],
    actuators=actuators,
    info_signals=info_sigs,
    md=md,
)
