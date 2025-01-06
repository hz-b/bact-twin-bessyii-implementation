from typing import Mapping, Sequence

from bact_twin_architecture.data_model.identifiers import ConversionID
from bact_twin_architecture.interfaces.state_conversion import StateConversion
from bact_twin_architecture.interfaces.translator_service import TranslatorServiceBase
from bact_twin_architecture.utils.unit_conversion import LinearUnitConversion


class TranslationService(TranslatorServiceBase):
    """
        Todo:
            currently the translation service only uses
            lattice id as its inputs, needs to be pushed forward
            to use ConversionID properly
    """
    def __init__(self, conversion_info: Sequence[object]):
         self.conversion_info = {item.conversion_id.lattice_property_id: item for item in conversion_info}

    def get(self, id_: ConversionID) -> StateConversion:
        linear_model = self.conversion_info[id_.lattice_property_id]
        return LinearUnitConversion(slope=linear_model.slope, intercept=linear_model.intercept)