import os
import subprocess

from utils import constants
from utils.command import build_analysis_command
from utils.common import extract_zip_to_temp_dir


# Polarion TC MTA-568
def test_hello_world_analysis_with_rules(dotnet_analysis_data):
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
            **{'rules': custom_rules_path}
        )

        output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

        assert 'Static report created' in output
