import pytest
from dotenv import load_dotenv

pytest_plugins = [
    "fixtures.analysis",
]


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()
