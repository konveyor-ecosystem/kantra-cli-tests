import json
import pytest


@pytest.fixture(scope="session")
def analysis_data():
    with open('data/analysis.json', 'r') as file:
        json_list = json.load(file)
    return json_list
