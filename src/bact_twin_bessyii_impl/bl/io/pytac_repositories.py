"""Loading files as typically used in pytac

**NB**: The element sequence id is not used here.
        The name of the lattice element is
        used as position name instead.

"""
from dataclasses import dataclass
from importlib.resources import files
import logging
from typing import Sequence, Union, Dict

import numpy as np
import pandas as pd
from bact_twin_architecture.data_model.identifiers import LatticeElementPropertyID, DevicePropertyID, ConversionID
from bact_twin_architecture.data_model.unit_conversion_info import LinearUnitConversionInfo

from bact_twin_bessyii_impl.bl.family_tree import ValidFamilyNames, BessyIIFamilyTree

logger = logging.getLogger("bact-twin-bessyii-impl")


def read_file(filename: str) -> pd.DataFrame:
    path = files("pytac") / "data" / "BESSY2" / filename
    return pd.read_csv(path)


def create_family_repository(
    element_names: Sequence[str],
    families_info : pd.DataFrame
):
    families = set(families_info.loc[:, "family"])

    def identifiers_of_family(selected_identifiers: pd.DataFrame) -> Sequence[str]:
        family_name, = set(selected_identifiers.family)
        # Dataframes ignore the first line, thus iloc is off by one
        # The csv files seem to use the line number
        # so we have reduce el_id by one
        assert (selected_identifiers.el_id > 0).all()
        r = [element_names[el_id - 1] for el_id in selected_identifiers.el_id]
        if not np.array([family_name in element_name for element_name in r], dtype=bool).all():
            logger.info(f"{family_name} not in all element names = '{r}'")
        return r

    return {
        family_name: identifiers_of_family(families_info.loc[families_info.family == family_name])
        for family_name in families
    }


@dataclass
class EPICSDeviceInfo:
    """
    Todo:
        is it general enough to be renamed DeviceInfo and
        moved to bact-twin-architecture
    """
    position_name: str
    device_name : str
    property : str
    setpoint: Union[str, None]
    readback: str


def convert_set_pv(value: Union[str, float]) -> Union[str, None]:
    if type(value) == type(1.0):
        assert np.isnan(value)
        return None
    return str(value)


def create_device_repository(
    element_names : Sequence[str],
    device_info: pd.DataFrame
):
    not_matched_devices = device_info.loc[device_info.el_id <= 0]
    if len(not_matched_devices) > 0:
        logger.error(f"I did not create a device repository for {not_matched_devices.loc[:, 'name']}")
    matched_devices = device_info.loc[device_info.el_id > 0]
    devices = [
        EPICSDeviceInfo(
            position_name=element_names[info.el_id-1],
            device_name=info.loc["name"],
            property=info.field,
            readback=info.get_pv,
            setpoint=convert_set_pv(info.set_pv)
        ) for _, info in matched_devices.iterrows()
    ]

    devices_property_mapping = dict()

    def update(info : EPICSDeviceInfo):
        identifier = info.device_name
        property = info.property
        try:
            devices_property_mapping[identifier]
        except KeyError:
            devices_property_mapping[identifier] = dict()
        devices_property_mapping[identifier][property] = info

    # build a dictionary of properties
    for device in devices:
        update(device)

    return devices_property_mapping


def create_state_conversion_repository(
        element_names : Sequence[str],
        poly_data_info : pd.DataFrame,
        unit_conv : pd.DataFrame,
        lattice_pos_to_device_mapping: Dict[str, Dict[str, str]]
):

    # for debugging purposes ... find an element in the list
    known_element_names = list(lattice_pos_to_device_mapping.keys())
    known_element_names.sort()

    def create_conversion(item: pd.Series):
        # not handling these special cases
        assert item.el_id > 0 and item.uc_id > 0
        elem_name = element_names[item.el_id - 1]
        t_coeffs = poly_data_info.loc[poly_data_info.uc_id == item.uc_id, :]
        intercept, = t_coeffs.loc[t_coeffs.coeff == 0, "val"].values
        slope, = t_coeffs.loc[t_coeffs.coeff == 1, "val"].values
        device_name = None
        lattice_pos_to_devices = None
        try:
            lattice_pos_to_devices = lattice_pos_to_device_mapping[elem_name]
        except KeyError:
            logger.error(f"Don't have any device info for lattice position {elem_name}")
        if lattice_pos_to_devices:
            try:
                device_name = lattice_pos_to_devices[item.field]
            except KeyError:
                logger.error(
                    f"Don't have any proper mapping {elem_name, item.field}",
                )
                logger.info(f"Known mappings for {elem_name} are: {lattice_pos_to_devices}")

        if device_name is None:
            pass
        return LinearUnitConversionInfo(
            conversion_id=ConversionID(
                lattice_property_id=LatticeElementPropertyID(element_name=elem_name, property=item.field),
                device_property_id=DevicePropertyID(device_name=device_name,property=None)
            ),
            slope=slope,
            intercept=intercept
        )

    r = [
        create_conversion(item)
        for _, item in unit_conv.iterrows() if item.el_id> 0 and item.uc_id> 0
    ]
    return r


def create_position_name_property_device_mapping(
        device_repo: Dict[str, Dict[str, EPICSDeviceInfo]]
) -> Dict[str, Dict[str, str]]:
    r = dict()
    def update(properties_info):
        for property, item in  properties_info.items():
            try:
                r[item.position_name]
            except KeyError:
                r[item.position_name] = dict()
            r[item.position_name][property] = item.device_name
    for _, item in device_repo.items():
        update(item)
    return r

class PyTACRepository:
    """

    Warning:
        Internally no position names are used but element number
        Thus be warned: any change in lattice will break all data
    """
    def __init__(self):
        minimal_lattice_info = read_file("elements.csv")
        lattice_element_names = minimal_lattice_info.loc[:, "name"]
        element_families = read_file("families.csv")

        epics_devices = read_file("epics_devices.csv")
        poly_data = read_file("uc_poly_data.csv")
        # Why are all coefficients of the first line zero?
        unit_conv = read_file("unitconv.csv")

        self.family_repo = create_family_repository(
            element_names=lattice_element_names,
            families_info=element_families
        )

        self.device_repo = create_device_repository(
            element_names=lattice_element_names,
            device_info=epics_devices
        )
        self.lattice_pos_to_device_mapping = create_position_name_property_device_mapping(self.device_repo)

        self.state_conversion_repo = create_state_conversion_repository(
            element_names=lattice_element_names,
            poly_data_info=poly_data,
            unit_conv=unit_conv,
            lattice_pos_to_device_mapping = self.lattice_pos_to_device_mapping
        )

def create_bessyii_family_tree(repo):
    families = {
        ValidFamilyNames.vertical_steerers.value: repo.family_repo["VCM"],
        # I decided: no dipole steerers in vertical steerers
        # as standard praxis at HZB
        ValidFamilyNames.horizontal_steerers.value: [
            name for name in repo.family_repo["HCM"] if not "BM" in name
        ],
    }
    return BessyIIFamilyTree(families=families)
