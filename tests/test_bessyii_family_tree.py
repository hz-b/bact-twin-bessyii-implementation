from bact_twin_bessyii_impl.bl.family_tree import PyTACBasedBessyIIFamilyTree
from bact_twin_bessyii_impl.bl.io.pytac_repositories import PyTACRepository

repo = PyTACRepository()

def test_load_data():
    """Todo: need to load pytac data properly
    """

    bessyii_family_tree = PyTACBasedBessyIIFamilyTree(repo)
    vt_sts = bessyii_family_tree.get("vertical_steerers")
    ht_sts = bessyii_family_tree.get("horizontal_steerers")
    all_sts = bessyii_family_tree.get("steerers")
    all_sts
