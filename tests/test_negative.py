import json
import subprocess

import pytest

from utils.command import build_analysis_command

with open("data/analysis.json", "r") as file:
    json_data = json.load(file)

# Getting first instance from JSON
first_entity_key = next(iter(json_data))


@pytest.mark.parametrize('app_name', [first_entity_key])
def test_analysis_wrong_target(app_name, analysis_data):
    application_data = analysis_data[app_name]

    # Building command to run
    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        "some_wrong_target"
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    # Making sure if we do have an error message about wrong label
    assert 'level=error msg=\"failed to create label selector from expression\" error=\"invalid expression' in output
