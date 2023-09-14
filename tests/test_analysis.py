import json
import subprocess

import pytest

from utils.command import build_analysis_command


@pytest.mark.parametrize('app_name', json.load(open("data/analysis.json")))
def test_standard_analysis(app_name, analysis_data):
    application_data = analysis_data[app_name]

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target']
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' in output
    # TODO: Assert report data
