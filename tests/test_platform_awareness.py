import glob
import os
import subprocess

from utils import constants
from utils.command import build_pa_discovery_command
from utils.asset_generation import compare_yaml_keys_and_values

# Polarion TC MTA-617
def test_cloudfoundry_local_discovery():
    input_yaml = os.path.join(os.getenv(
        constants.PROJECT_PATH), 'data', 'yaml', 'asset_generation', 'cf-nodejs-app.yaml')
    output_dir = './output_dir'

    command = build_pa_discovery_command(input_yaml,
        **{'output-dir': output_dir}
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE,
        encoding='utf-8').stdout
    assert 'Writing content to file' in output, f"Discovery command failed"

    yaml_files = glob.glob(f'{output_dir}/*.yaml')
    assert yaml_files, f"Discovery manifest was not generated {output_dir}"

    # Validate discovery manifest
    output_yaml = yaml_files[0]
    result = compare_yaml_keys_and_values(input_yaml, output_yaml)
    print("Extra keys in output YAML:")
    for key in sorted(result["extra_keys_in_output"]):
        print("  ", key)

    print("\nMissing keys in output YAML:")
    for key in sorted(result["missing_keys_in_output"]):
        print("  ", key)

    print("\nMismatched values in output YAML:")
    for value in sorted(result["mismatched_values"]):
        print("  ", value)
