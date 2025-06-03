import os
import subprocess

from utils import constants
from utils.command import build_analysis_command
from utils.report import assert_story_points_from_report_file, get_json_from_report_output_file


def test_python_analysis_with_rules(python_analysis_data):
    application_data = python_analysis_data["python_app_project"]
    application_path = os.path.join(
        os.getenv(constants.PROJECT_PATH),
        'data',
        'applications',
        application_data['file_name']
    )
    custom_rules_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data','yaml', 'python_rules.yaml')

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{'provider': "go",
            'rules': custom_rules_path,
           "--run-local=false": None}
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    report_data = get_json_from_report_output_file()
    ruleset = next((item for item in report_data['rulesets'] if item.get('description') == 'temp ruleset'), None)


    assert 'generating static report' in output
    assert ruleset is not None, "Ruleset property not found in output"
    assert len(ruleset.get('skipped', [])) == 0, "Custom Rule was skipped"
    assert 'violations' in ruleset, "Custom rules didn't trigger any violation"