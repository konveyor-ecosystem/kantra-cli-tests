import os
import subprocess

from utils import constants
from utils.command import build_analysis_command
from utils.common import verify_triggered_rules
from utils.report import get_json_from_report_output_file


def test_python_analysis_with_rules(python_analysis_data):
    application_data = python_analysis_data["python_app_project"]

    custom_rules_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data','yaml', 'python_rules.yaml')

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{'provider': "python",
            'rules': custom_rules_path,
           "--run-local=false": None}
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    report_data = get_json_from_report_output_file()



    assert 'generating static report' in output

    verify_triggered_rules(report_data, ['python-sample-rule-001', 'python-sample-rule-002'], 1)

