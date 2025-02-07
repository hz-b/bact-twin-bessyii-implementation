from typing import Sequence


class YellowPages:
    def __init__(self, d: dict):
        self._d = d

    def horizontal_steerer_names(self) -> Sequence[str]:
        return self._d["horizontal_steerer_names"]

    def vertical_steerer_names(self) -> Sequence[str]:
        return self._d["vertical_steerer_names"]

    def quadrupole_names(self) -> Sequence[str]:
        return self._d["quadrupole_names"]

    def sextupole_names(self) -> Sequence[str]:
        return self._d["sextupole_names"]


def bessyii_yellow_pages():
    # standard quadrupoles
    quadrupoles = [
        f"Q{family}M{child}{sector_type}{sector}R"
        for family in range(1, 6)
        for child in range(1, 3)
        for sector_type in ["D", "T"]
        for sector in range(1, 9)
    ]
    # Emil straight
    quadrupoles += ["QIT6R"]

    sextupoles = [
        f"S{family}M{sector_type}{sector}R"
        for family in range(1, 2)
        for sector_type in ["D", "T"]
        for sector in range(1, 9)
    ]
    sextupoles += [
        f"S{family}M{child}{sector_type}{sector}R"
        for family in range(2, 6)
        for child in range(1, 3)
        for sector_type in ["D", "T"]
        for sector in range(1, 9)
    ]
    horizontal_steerers = [
        f"H{sextupole}" for sextupole in sextupoles if sextupole[1] in ["1", "4"]
    ]
    vertical_steerers = [
        f"V{sextupole}" for sextupole in sextupoles if sextupole[1] in ["2", "3"]
    ]
    d = dict(
        quadrupole_names=quadrupoles,
        sextupole_names=sextupoles,
        horizontal_steerer_names=horizontal_steerers,
        vertical_steerer_names=vertical_steerers,
    )

    return YellowPages(d)


yp = bessyii_yellow_pages()


def name_matches_horizontal_steerer_name(name):
    flag = name_matches_steerer_name(name) and name[0] == "H"
    if flag and name not in yp.horizontal_steerer_names():
        pass
    return flag


def name_matches_vertical_steerer_name(name: str) -> bool:
    """
    Todo:
        just use yp for lookup
    """
    flag = name_matches_steerer_name(name) and name[0] == "V"
    if flag and name not in yp.vertical_steerer_names():
        pass
    return flag


def name_matches_steerer_name(name):
    if name[:2] not in ("HS", "VS"):
        return False
    if name[1:] in yp.sextupole_names():
        return True
    return False


def name_matches_quadrupole_name(name):
    if name[0] != "Q":
        return False
    if name not in yp.quadrupole_names():
        return False
    return True


def name_matches_sextupole_name(name):
    if name[0] != "S":
        return False
    if name not in yp.sextupole_names():
        return False
    return True


def suffix_matches_magnet_suffix(suffix):
    if int(suffix[0]) not in (1, 2, 3, 4, 5):
        return False
    if suffix[1] != "M":
        return False
    if int(suffix[2]) not in (1, 2):
        return False
    if suffix[-3] not in ["D", "T"]:
        return False
    if int(suffix[-2]) not in (1, 2, 3, 4, 5, 6, 7, 8):
        return False
    if suffix[-1] != "R":
        return False
    return True


def steerer_name_to_host_magnet_name(name):
    assert name_matches_steerer_name(name)
    return name[1:]
