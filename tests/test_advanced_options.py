import os
import signal
import subprocess
import time

from utils import constants
from utils.command import build_analysis_command, build_discovery_command
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
    verify_triggered_rule(report_data, ['Test-002-00001'])

# Automates Bug 4784
def test_description_display_in_report(analysis_data):
    application_data = analysis_data['jee_example_app']

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        ""
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' in output
    assert_story_points_from_report_file()

    report_data = get_json_from_report_output_file()
    ruleset = next(
        (ruleset for ruleset in report_data["rulesets"] if "singleton-sessionbean-00001" in ruleset.get("violations", {})),
        None
    )
    assert ruleset is not None, "The expected rule was not triggered"
    assert "When a singleton EJB bean class implements `javax.ejb.SessionBean` interface" in ruleset["violations"]["singleton-sessionbean-00001"]["description"], "The reported issue did not include the description"


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


def test_language_discovery(analysis_data, python_analysis_data, golang_analysis_data, nodejs_analysis_data):
    applications_data = [
        analysis_data['tackle-testapp-public'],
        python_analysis_data["python_app_project"],
        golang_analysis_data["golang_app"],
        nodejs_analysis_data["nodejs_app_project"]
    ]
    for application_data in applications_data:
        command = build_discovery_command(application_data['file_name'])
        output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout
        for language in application_data["languages"]:
            assert language in output, f"Language {language} was not detected in the {application_data['app_name']} app"


def test_custom_rules_disable_default(analysis_data):
    application_data = analysis_data['tackle-testapp-project']
    assert os.getenv(constants.PROJECT_PATH) is not None
    custom_rule_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data', 'yaml', 'test-rules')

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{
            'rules': custom_rule_path,
            'enable-default-rulesets': 'false'
        }
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' in output
    assert_story_points_from_report_file()

    expected_rule_id_list = [
        'basic-location-001',
        'basic-location-002',
        'basic-location-003',
        'basic-location-004',
        'basic-location-005',
        'basic-location-006',
        'basic-location-007',
        'basic-location-008',
        'basic-location-009',
        'basic-location-010',
        'basic-location-011',
        'basic-location-012',
        'basic-location-013',
        'basic-location-014',
        'basic-location-015',
        'basic-location-016',
        'basic-location-017',
        'basic-location-018',
        'basic-location-019',
        'basic-location-020'
    ]

    report_data = get_json_from_report_output_file()
    verify_triggered_rule(report_data, expected_rule_id_list)