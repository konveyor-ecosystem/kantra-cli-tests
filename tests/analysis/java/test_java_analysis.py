import json
import os
import subprocess

import pytest

from utils import constants
from utils.command import build_analysis_command
from utils.common import run_containerless_parametrize, verify_triggered_rule
from utils.manage_maven_credentials import manage_credentials_in_maven_xml
from utils.report import assert_story_points_from_report_file, get_json_from_report_output_file

@run_containerless_parametrize
@pytest.mark.parametrize('app_name', json.load(open("data/analysis.json")))
def test_standard_analysis(app_name, analysis_data, additional_args):
    application_data = analysis_data[app_name]

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **additional_args
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' in output

    assert_story_points_from_report_file()


def test_dependency_rule_analysis(analysis_data):
    application_data = analysis_data['tackle-testapp-project']
    custom_maven_settings = os.path.join(
        os.getenv(constants.PROJECT_PATH),
        'data/xml',
        'tackle-testapp-public-settings.xml'
    )
    custom_rule_path = os.path.join(
        os.getenv(constants.PROJECT_PATH),
        'data/yaml',
        'tackle-dependency-custom-rule.yaml'
    )
    manage_credentials_in_maven_xml(custom_maven_settings)

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        "",
        **{
            'maven-settings': custom_maven_settings,
            'rules': custom_rule_path,
        }
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    manage_credentials_in_maven_xml(custom_maven_settings, True)

    assert 'generating static report' in output

    report_data = get_json_from_report_output_file()

    verify_triggered_rule(report_data, 'tackle-dependency-test-rule')
