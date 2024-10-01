from bact_twin_bessyii_impl.bl.io.pytac_repositories import PyTACRepository


def test_pytac_repo_load():
    """just check that it loads the repositories

    """
    repo = PyTACRepository()
    repo.device_repo
    repo.family_repo
