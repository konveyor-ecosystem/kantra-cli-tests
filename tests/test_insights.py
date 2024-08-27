import os
import subprocess

from utils import constants
from utils.command import build_analysis_command
from utils.report import assert_insights_from_report_file

# Polarion TC 598
def test_insights_binary_app(analysis_data):
    application_data = analysis_data['jee_example_app']
    custom_rule_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/xml', 'weblogic-custom.windup.yaml')

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target']
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' in output
    assert_insights_from_report_file()

# Polarion TC 374
def test_custom_rules(analysis_data):
    application_data = analysis_data['tackle-testapp-project']
    custom_rule_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/yaml', 'custom_rule_insights.yaml')

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{'rules': custom_rule_path}
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' in output
    assert_insights_from_report_file()
