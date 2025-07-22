import os
import subprocess

from utils import constants
from utils.command import build_analysis_command
from utils.common import verify_triggered_yaml_rules
from utils.report import assert_story_points_from_report_file, get_dict_from_output_yaml_file

# Polarion TC MTA-536, 543
def test_java_provider_analysis(analysis_data):

    application_data = analysis_data['tackle-testapp-project']
    custom_rules_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/yaml', '01-javax-package-custom-target.windup.yaml')
    command = build_analysis_command(
            application_data['file_name'],
            application_data['source'],
            application_data['target'],
            **{'provider': "java",
               'rules': custom_rules_path}
        )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'Static report created' in output
    
    assert_story_points_from_report_file()

    report_data = get_dict_from_output_yaml_file()

    verify_triggered_yaml_rules(report_data, ['javax-package-custom-target-00001'], True)

