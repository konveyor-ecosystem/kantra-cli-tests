import os
import subprocess

from utils import constants
from utils.command import build_analysis_command
from utils.manage_maven_credentials import manage_credentials_in_maven_xml
from utils.report import assert_story_points_from_report_file, get_json_from_report_output_file, clearReportDir


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
def test_custom_rules(analysis_data):
    application_data = analysis_data['jee_example_app']
    custom_rule_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/xml', 'weblogic-custom.windup.yaml')

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

    ruleset = next((item for item in report_data['rulesets'] if item.get('description') == 'temp ruleset'), None)

    assert ruleset is not None, "Ruleset property not found in output"
    assert len(ruleset.get('skipped', [])) == 0, "Custom Rule was skipped"
    assert len(ruleset.get('unmatched', [])) == 0, "Custom Rule was unmatched"
    assert 'violations' in ruleset, "Custom rules didn't trigger any violation"
    assert 'weblogic-xml-custom-rule' in ruleset['violations'], "weblogic-xml-custom-rule triggered no violations"


def test_bulk_analysis(analysis_data):
    applications = [analysis_data['administracion_efectivo'], analysis_data['jee_example_app']]
    clearReportDir()

    for application in applications:
        command = build_analysis_command(
            application['file_name'],
            application['source'],
            application['target'],
            True
        )
        output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

        assert 'generating static report' in output

    report_data = get_json_from_report_output_file(False)
    assert len(report_data) >= 2, "Less than 2 application analysis detected"
    for current_report in report_data:
        assert len(current_report['rulesets']) >= 0, "No rulesets were applied"
        assert len(current_report['depItems']) >= 0, "No dependencies were found"
        violations = [item for item in current_report['rulesets'] if item.get('violations')]
        assert len(violations) > 0, "No issues were found";

# Validation for Jira ticket MTA-3779
def test_analysis_of_private_repo(analysis_data):
    application_data = analysis_data['tackle-testapp-public']
    custom_maven_settings = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/xml', 'tackle-testapp-public-settings.xml')
    manage_credentials_in_maven_xml(custom_maven_settings)
    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{'maven-settings': custom_maven_settings}
    )
    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout
    assert 'generating static report' in output

    report_data = get_json_from_report_output_file(False)
    assert len(report_data[0]['depItems']) >= 0, "No dependencies were found"
    violations = [item for item in report_data[0]['rulesets'] if item.get('violations')]
    assert len(violations) > 1, "Expected issues are missing";

    manage_credentials_in_maven_xml(custom_maven_settings, True)
