import os
import subprocess

from utils import constants
from utils.command import build_analysis_command
from utils.report import get_json_from_report_output_file


# Polarion TC MTA-542
def test_nodejs_provider_analysis(nodejs_analysis_data):
    application_data = nodejs_analysis_data['nodejs_app_project']
    custom_rules_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/yaml', 'python_rules.yaml')
    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{'rules': custom_rules_path,
           'provider': "nodejs"}
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'Static report created' in output
