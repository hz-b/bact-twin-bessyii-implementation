import json
from bact_twin_architecture.data_model.command import Command, CommandSequence
from bact_twin_architecture.bl.bluesky_measurement_engine import BlueskyMeasurementExecutinEngine

import bluesky


with open("orm_commands.json") as fp:
    tmp = json.load(fp)
cmds = CommandSequence(commands=[Command(**d) for d in tmp["commands"]])

RE = bluesky.run_engine.RunEngine()
mexec = BlueskyMeasurementExecutinEngine()
