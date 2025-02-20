import time
import pytest
from dotenv import load_dotenv

pytest_plugins = [
    "fixtures.analysis",
    "fixtures.transformation",
]


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()

def pytest_runtest_setup(item):
    item.start_time = time.perf_counter()

def pytest_runtest_teardown(item):
    duration = time.perf_counter() - item.start_time
    print(f"\nTest {item.name} took {duration:.4f} seconds")