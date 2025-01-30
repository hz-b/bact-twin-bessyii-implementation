def name_matches_horizontal_steerer_name(name):
    return name_matches_steerer_name(name) and name[0] == "H"

def name_matches_vertical_steerer_name(name):
    return name_matches_steerer_name(name) and name[0] == "V"

def name_matches_steerer_name(name):
    if name[:2] not in ("HS", "VS"):
        return False

    if name[2] == "P":
        return name[3] in ("1", "2")

    elif name[2] in ("1", "2", "3", "4"):
        return True
    else:
        return False

def steerer_name_to_host_magnet_name(name):
    assert name_matches_steerer_name(name)
    return name[1:]