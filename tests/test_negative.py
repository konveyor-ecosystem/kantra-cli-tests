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

    # Run the command
    process = subprocess.run(
        command,
        shell=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'
    )

    # Check if the return code indicates an error
    assert process.returncode != 0

    # Check if the error message contains the expected text
    assert 'failed to load provider settings open /opt/output/output.yaml: no such file or directory' in process.stderr
