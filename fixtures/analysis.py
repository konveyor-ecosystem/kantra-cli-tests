import json
import pytest

@pytest.fixture(scope="session")
def analysis_data():
    with open('data/analysis.json', 'r') as file:
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
