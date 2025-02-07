from bact_twin_bessyii_impl.bl.bessyii_nomen_clature import bessyii_yellow_pages


def test_yellow_pages_quadrpole_names():
    yp = bessyii_yellow_pages()
    assert "Q1M1D1R" in yp.quadrupole_names()
    assert "QIT6R" in yp.quadrupole_names()

def test_yellow_pages_sextupole_names():
    yp = bessyii_yellow_pages()
    assert "S1MT1R" in yp.sextupole_names()
    assert "S1MD2R" in yp.sextupole_names()


def test_yellow_pages_horizontal_steerer_names():
    yp = bessyii_yellow_pages()
    assert "HS1MD1R" in yp.horizontal_steerer_names()
    assert "HS4M1T1R" in yp.horizontal_steerer_names()


def test_yellow_pages_vertical_steerer_names():
    yp = bessyii_yellow_pages()
    assert "VS2M1D1R" in yp.vertical_steerer_names()
    assert "VS3M1T1R" in yp.vertical_steerer_names()