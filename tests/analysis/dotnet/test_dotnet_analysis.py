import os
import subprocess

from utils import constants
from utils.command import build_analysis_command
from utils.common import extract_zip_to_temp_dir, verify_triggered_rule
from utils.report import assert_story_points_from_report_file, get_json_from_report_output_file


# Polarion TC MTA-568
def test_hello_world_linux_analysis_with_rules(dotnet_analysis_data):
    # Avoid running this test on Windows
    if os.name == 'nt':
        return

    application_data = dotnet_analysis_data["hello_world"]
    application_path = os.path.join(
        os.getenv(constants.PROJECT_PATH),
        'data/applications',
        application_data['file_name']
    )
    custom_rules_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/yaml/dotnet/example_rules')

    with extract_zip_to_temp_dir(application_path) as tempdir:
        command = build_analysis_command(
            tempdir,
            "",
            "",
            **{
                'rules': custom_rules_path,
                'run-local': 'false',
                'provider': 'dotnet'
            }
        )

        output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

        assert 'Static report created' in output
        assert_story_points_from_report_file()
        report_data = get_json_from_report_output_file()
        verify_triggered_rule(report_data, 'custom-rule-dotnet-framework')
