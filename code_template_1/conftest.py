from __future__ import print_function
from pytest import fixture


@fixture
def global_fixture():
    """
    Fixture for global setup.

    This function is a fixture that is executed once before any tests in the test suite.
    It performs global setup tasks, such as initializing resources or setting up the environment.

    Parameters:
        None

    Returns:
        None
    """
    print("\n(Doing global fixture setup stuff!)")


def pytest_configure(config):
    """
    Add markers to the pytest configuration.

    Args:
        config (object): The pytest configuration object.

    Returns:
        None
    """
    config.addinivalue_line(
        "markers", "db: Example marker for tagging Database related tests"
    )
    config.addinivalue_line(
        "markers", "slow: Example marker for tagging extremely slow tests"
    )
