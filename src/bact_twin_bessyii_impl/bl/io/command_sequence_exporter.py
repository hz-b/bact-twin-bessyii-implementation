import json

from bact_twin_architecture.data_model.command import Command, CommandSequence
from typing import Sequence
from dataclasses import asdict
import jsons

def commands_to_json(commands: Sequence[Command]):
    return jsons.dump(asdict(CommandSequence(commands=commands)))

def export_commands(commands: Sequence[Command], fp):
    json.dump(commands_to_json(commands=commands), fp, indent=2)