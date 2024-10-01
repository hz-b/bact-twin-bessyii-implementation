import pytest
from bact_twin_bessyii_impl.bl.io.pytac_repositories import PyTACRepository


def test_pytac_repo_load():
    """just check that it loads
    """
    repo = PyTACRepository()
    r = repo.get("vertical_steerers")
    print(r)