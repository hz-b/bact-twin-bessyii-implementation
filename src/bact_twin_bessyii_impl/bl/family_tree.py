"""

"""
from enum import Enum

from bact_twin_architecture.interfaces.family_tree import FamilyTree


class ValidFamilyNames(Enum):
    """Valid family name
    """
    horizontal_steerers = "horizontal_steerers"
    vertical_steerers = "vertical_steerers"
    steerers = "steerers"


class BessyIIFamilyTree(FamilyTree):
    """
    """
    def __init__(self):
        self.families = dict()
        raise NotImplementedError("Use derived class")

    def get(self, family_name: str):
        bessyii_family_name = ValidFamilyNames(family_name)
        if bessyii_family_name == ValidFamilyNames.steerers:
            return (
                    self.families[ValidFamilyNames.horizontal_steerers.value] +
                    self.families[ValidFamilyNames.vertical_steerers.value]
            )
        else:
            return self.families[bessyii_family_name.value]


class PyTACBasedBessyIIFamilyTree(BessyIIFamilyTree):
    def __init__(self, repo):
        self.families = {
            ValidFamilyNames.vertical_steerers.value : repo.family_repo["VCM"],
            # I decided: no dipole steerers in vertical steerers
            # as standard praxis at HZB
            ValidFamilyNames.horizontal_steerers.value : [name for name in repo.family_repo["HCM"] if not "BM" in name],
        }

