import os
import subprocess

from utils.command import build_analysis_command

# Polarion TC MTA-536
def test_java_provider_analysis_with_app(analysis_data):

    application_data = analysis_data['jee_example_app']
    command = build_analysis_command(
            application_data['file_name'],
            "",
            "eap8",
            **{'provider': "java"}
        )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'Static report created' in output
    
    assert_story_points_from_report_file()
