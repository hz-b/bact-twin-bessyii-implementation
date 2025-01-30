from bact_twin_architecture.data_model.identifiers import DevicePropertyID

from bact_twin_bessyii_impl.bl.liaison_manager import LiaisonManager


def test_managing_steerers():
    mger = LiaisonManager()
    cmd, = mger.inverse(DevicePropertyID("HSP1D1R", "set_current"))
    assert cmd.property == "x_kick"
    assert cmd.element_name == "SM1D1R"

    cmd, = mger.inverse(DevicePropertyID("HS4P1D1R", "set_current"))
    assert cmd.property == "x_kick"
    assert cmd.element_name == "S4M1D1R"


def test_managing_master_clock():
    mger = LiaisonManager()
    cmds = mger.inverse(DevicePropertyID("MCLKHX251C", "reference_frequency"))
    for cmd in cmds:
        assert cmd.property == "frequency"
        assert cmd.element_name[:3] == "CAV"
