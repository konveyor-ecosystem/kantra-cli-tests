import os
import signal
import subprocess
import time

from utils import constants
from utils.command import build_analysis_command
from utils.common import run_containerless_parametrize, verify_triggered_rule
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
    custom_rule_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data', 'yaml', '01-test-jee.windup.yaml')

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
    verify_triggered_rule(report_data, 'Test-002-00001')


@run_containerless_parametrize
def test_bulk_analysis(analysis_data, additional_args):
    applications = [analysis_data['administracion_efectivo'], analysis_data['jee_example_app']]
    clearReportDir()

    for application in applications:
        command = build_analysis_command(
            application['file_name'],
            application['source'],
            application['target'],
            True,
            **additional_args
        )
        output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

        assert 'generating static report' in output

    report_data = get_json_from_report_output_file(False)
    assert len(report_data) >= 2, "Less than 2 application analysis detected"
    for current_report in report_data:
        assert len(current_report['rulesets']) >= 0, "No rulesets were applied"
        assert len(current_report['depItems']) >= 0, "No dependencies were found"
        violations = [item for item in current_report['rulesets'] if item.get('violations')]
        assert len(violations) > 0, "No issues were found"


# Validation for Jira ticket MTA-3779
@run_containerless_parametrize
def test_analysis_of_private_repo(analysis_data, additional_args):
    application_data = analysis_data['tackle-testapp-public']
    custom_maven_settings = os.path.join(
        os.getenv(constants.PROJECT_PATH),
        'data/xml',
        'tackle-testapp-public-settings.xml'
    )
    manage_credentials_in_maven_xml(custom_maven_settings)

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{'maven-settings': custom_maven_settings},
        **additional_args
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout
    assert 'generating static report' in output

    report_data = get_json_from_report_output_file(False)
    assert len(report_data[0]['depItems']) >= 0, "No dependencies were found"
    violations = [item for item in report_data[0]['rulesets'] if item.get('violations')]
    assert len(violations) > 1, "Expected issues are missing";

    manage_credentials_in_maven_xml(custom_maven_settings, True)


def test_no_container_leftovers(analysis_data):
    application_data = analysis_data['jee_example_app']
    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{"--run-local=": "false"} # Checking for container leftovers only if running in container mode
    )
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

    time.sleep(10)
    process.send_signal(signal.SIGINT)

    process.wait()

    leftover = subprocess.run("podman ps", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    leftover_output = leftover.stdout.strip()

    for line in leftover_output.splitlines():
        assert "analysis-" not in line, f"Found a leftover analysis container: \n{line}"
        assert "provider-" not in line, f"Found a leftover provider container: \n {line}"
