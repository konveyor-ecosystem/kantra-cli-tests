import pytest
from dotenv import load_dotenv

pytest_plugins = [
    "fixtures.analysis",
    "fixtures.transformation",
]


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()
