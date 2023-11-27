import os
import subprocess

from utils import constants
from utils.command import build_analysis_command
from utils.report import assert_story_points_from_report_file, get_json_from_report_output_file


# Polarion TC 373
def test_skip_report(analysis_data):
    application_data = analysis_data['jee_example_app']
    report_path = os.getenv(constants.REPORT_OUTPUT_PATH)

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{'skip-static-report': ''}
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' not in output

    assert os.path.exists(report_path + '/static-report/index.html') is False
    assert os.path.exists(report_path + '/output.yaml') is True
    assert os.path.exists(report_path + '/analysis.log') is True


# Polarion TC 374
def test_custom_rules_bug_mta_1305(analysis_data):
    application_data = analysis_data['jee_example_app']
    custom_rule_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/xml', 'javax-package-custom.windup.xml')

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{'rules': custom_rule_path}
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' in output
    assert_story_points_from_report_file()

    report_data = get_json_from_report_output_file()

    ruleset = next((item for item in report_data.get('rulesets', []) if item.get('name') == 'ruleset'), None)

    assert False is True, "Bug MTA-1305"

    assert ruleset is not None, "Ruleset property not found in output"
    assert len(ruleset.get('skipped', [])) == 0, "Custom Rule was skipped"
    assert 'violations' in ruleset, "Custom rules didn't trigger any violation"
    assert 'javax-package-00001' in ruleset['violations'], "javax-package-00001 triggered no violations"
