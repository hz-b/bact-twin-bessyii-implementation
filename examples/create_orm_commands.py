import itertools

from bact_twin_architecture.data_model.command import Command, BehaviourOnError
from bact_twin_bessyii_impl.bl.io.command_sequence_exporter import export_commands
from bact_twin_bessyii_impl.bl.io.pytac_repositories import (
    PyTACRepository,
    create_bessyii_family_tree,
)

bessyii_family_tree = create_bessyii_family_tree(PyTACRepository())

vertical_corrector_ids = bessyii_family_tree.get("vertical_steerers")

measurement_values = [0, 1e-4, 0, -1e-4, 0]
commands = [
    Command(
        id=corr, property="y_kick", value=val, behaviour_on_error=BehaviourOnError.stop
    )
    for corr, val in itertools.product(vertical_corrector_ids, measurement_values)
]
with open("orm_commands.json", "wt") as fp:
    export_commands(commands, fp)
