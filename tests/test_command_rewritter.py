from bact_twin_architecture.data_model.command import Command, BehaviourOnError

from bact_twin_bessyii_impl.bl.command_rewritter import CommandRewriter
from bact_twin_bessyii_impl.bl.translation_service import TranslationService


def setup():
    """

    Todo:
        design a dedicated test repository

    """
    from bact_twin_bessyii_impl.bl.io.pytac_repositories import PyTACRepository

    repo = PyTACRepository()
    return CommandRewriter(TranslationService(conversion_info=repo.state_conversion_repo))

def test_rewrite_steerers():
    rewriter = setup()
    ncmd, = rewriter.inverse(Command(id="HS4P1D1R", property="set_current", value=0.0, behaviour_on_error=BehaviourOnError.stop))
    ncmd
    rewriter = setup()
    ncmd, = rewriter.inverse(Command(id="VS3P2T7R", property="set_current", value=0.0, behaviour_on_error=BehaviourOnError.stop))
    ncmd
    rewriter = setup()
    ncmd, = rewriter.inverse(Command(id="S3M2T7R", property="K", value=0.0, behaviour_on_error=BehaviourOnError.stop))
    ncmd

def test_rewrite_master_clock():
    rewriter = setup()
    ncmds = rewriter.inverse(Command(id="MCLKHX251C", property="reference_frequency", value=0.0, behaviour_on_error=BehaviourOnError.stop))
    ncmds