import json
import pprint

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

def ci_data():
    with open('data/ci/shared_tests/test_cases.yml', 'r') as file:
        extracted_data = []
        ci_test_cases = yaml.safe_load(file)
        for tc_name in ci_test_cases.keys():
            tc = ci_test_cases[tc_name]
            tc['referencesDir'] = tc['name'] = tc_name
            extracted_data.append(tc)
        return extracted_data