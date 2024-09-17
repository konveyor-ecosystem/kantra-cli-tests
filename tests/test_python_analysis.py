import os
import subprocess

from utils import constants
from utils.command import build_analysis_command
from utils.report import assert_story_points_from_report_file, get_json_from_report_output_file


# Polarion TC MTA-541
def bug_mta_3821_test_python_provider_analysis(python_analysis_data):
    application_data = python_analysis_data['python_app_project']
    custom_rules_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/yaml', 'python_rules.yaml')

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{'provider': "python",
            'rules': custom_rules_path}
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' in output
    assert_story_points_from_report_file()

    report_data = get_json_from_report_output_file()

    ruleset = next((item for item in report_data['rulesets'] if item.get('description') == 'temp ruleset'), None)

    assert ruleset is not None, "Ruleset property not found in output"
    assert len(ruleset.get('skipped', [])) == 0, "Custom Rule was skipped"
    assert len(ruleset.get('unmatched', [])) == 0, "Custom Rule was unmatched"
    assert 'violations' in ruleset, "Custom rules didn't trigger any violation"
    assert 'python-sample-rule-001' in ruleset['violations'], "python-sample-rule-001 triggered no violations"
    assert 'python-sample-rule-002' in ruleset['violations'], "python-sample-rule-002 triggered no violations"