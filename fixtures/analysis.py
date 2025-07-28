import json
import pytest
import yaml


@pytest.fixture(scope="session")
def analysis_data():
    with open('data/analysis.json', 'r') as file:
        json_list = json.load(file)
    return json_list

@pytest.fixture(scope="session")
def java_analysis_data():
    with open('data/java_analysis.json', 'r') as file:
        json_list = json.load(file)
    return json_list

@pytest.fixture(scope="session")
def dotnet_analysis_data():
    with open('data/dotnet_analysis.json', 'r') as file:
        json_list = json.load(file)
    return json_list

@pytest.fixture(scope="session")
def golang_analysis_data():
    with open('data/golang_analysis.json', 'r') as file:
        json_list = json.load(file)
    return json_list

@pytest.fixture(scope="session")
def nodejs_analysis_data():
    with open('data/nodejs_analysis.json', 'r') as file:
        json_list =  json.load(file)
    return json_list

@pytest.fixture(scope="session")
def python_analysis_data():
    with open('data/python_analysis.json', 'r') as file:
        json_list = json.load(file)
    return json_list

@pytest.fixture(scope="session")
def book_server_data():
    with open('data/ci/shared_tests/analysis_book-server/tc.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data