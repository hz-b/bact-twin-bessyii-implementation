"""Demonstrator of handling families of devices

Currently providing lookup for horizontal and
vertical steerers

Todo:
   review which part should be moved to architecture
   or reference implementation
"""
from enum import Enum

from bact_twin_architecture.interfaces.family_tree import FamilyTree


class ValidFamilyNames(Enum):
    """Valid family name"""

    horizontal_steerers = "horizontal_steerers"
    vertical_steerers = "vertical_steerers"
    steerers = "steerers"


class BessyIIFamilyTree(FamilyTree):
    """Some first families"""

    def __init__(self, families):
        self.families = families

    def get(self, family_name: str):
        bessyii_family_name = ValidFamilyNames(family_name)
        if bessyii_family_name == ValidFamilyNames.steerers:
            return (
                self.families[ValidFamilyNames.horizontal_steerers.value]
                + self.families[ValidFamilyNames.vertical_steerers.value]
            )
        else:
            return self.families[bessyii_family_name.value]
