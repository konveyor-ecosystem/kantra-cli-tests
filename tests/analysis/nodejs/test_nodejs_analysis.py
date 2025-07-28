import os
import subprocess

from utils import constants
from utils.command import build_analysis_command


# Polarion TC MTA-542
def test_nodejs_provider_analysis(nodejs_analysis_data):
    application_data = nodejs_analysis_data['nodejs_app_project']
    # TODO: replace with a nodejs rule when available and validate them
    custom_rules_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/yaml', 'python_rules.yaml')
    command = build_analysis_command(
        application_data['file_name'],
        application_data['sources'],
        application_data['targets'],
        **{'rules': custom_rules_path,
           'provider': "nodejs"}
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'Static report created' in output
