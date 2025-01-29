from bact_twin_architecture.data_model.identifiers import DevicePropertyID

from bact_twin_bessyii_impl.bl.liaison_manager import LiaisonManager


def test_liaison_manager():
    mger = LiaisonManager()
    cmd = mger.inverse(DevicePropertyID("HSP1D1R", "set_current"))
    assert cmd.property == "x_kick"
    assert cmd.element_name == "SM1D1R"

    cmd = mger.inverse(DevicePropertyID("HS4P1D1R", "set_current"))
    assert cmd.property == "x_kick"
    assert cmd.element_name == "S4M1D1R"