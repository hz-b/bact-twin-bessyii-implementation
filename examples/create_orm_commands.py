import itertools

from bact_twin_architecture.data_model.command import Command, BehaviourOnError
from bact_twin_bessyii_impl.bl.io.command_sequence_exporter import export_commands
from bact_twin_bessyii_impl.bl.io.pytac_repositories import (
    PyTACRepository,
    create_bessyii_family_tree,
)

bessyii_family_tree = create_bessyii_family_tree(PyTACRepository())

vertical_steerer_ids = bessyii_family_tree.get("vertical_steerers")
horizontal_steerer_ids = bessyii_family_tree.get("horizontal_steerers")

measurement_values = [0, .1, 0, -.1, 0]
commands = [
    Command(
        id=corr, property="y_kick", value=val, behaviour_on_error=BehaviourOnError.stop
    )
    for corr, val in itertools.product(vertical_steerer_ids, measurement_values)
]
commands += [
    Command(
        id=corr, property="x_kick", value=val, behaviour_on_error=BehaviourOnError.stop
    )
    for corr, val in itertools.product(horizontal_steerer_ids, measurement_values)
]
with open("orm_commands.json", "wt") as fp:
    export_commands(commands, fp)
