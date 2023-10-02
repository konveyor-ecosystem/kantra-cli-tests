import json
import pytest


@pytest.fixture(scope="session")
def openrewrite_transformation_data():
    with open('data/openrewrite_transformation.json', 'r') as file:
        json_list = json.load(file)
    return json_list
