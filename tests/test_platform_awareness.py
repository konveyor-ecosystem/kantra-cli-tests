import glob
import os
import subprocess
from pathlib import Path

from utils import constants
from utils.command import build_pa_discovery_command
from utils.asset_generation import compare_yaml_keys_and_values

# Polarion TC MTA-617
def test_cloudfoundry_local_discovery():
    input_yaml = os.path.join(os.getenv(
        constants.PROJECT_PATH), 'data', 'yaml', 'asset_generation', 'cf-nodejs-app.yaml')
    output_dir = os.path.join(os.getenv(constants.PROJECT_PATH), 'output_dir')

    command = build_pa_discovery_command(input_yaml,
        **{'output-dir': output_dir}
    )

    # Perform discovery of locally stored application manifest
    # Input: CloudFoundry application manifest, Output: Discovery manifest
    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE,
        encoding='utf-8').stdout
    assert 'Writing content to file' in output, f"Discovery command failed"

    dir_path = Path(output_dir)
    assert dir_path.exists() and dir_path.is_dir(), f"Output directory '{dir_path}' was not created"

    yaml_files = glob.glob(f'{output_dir}/*.yaml')
    assert yaml_files, f"Discovery manifest was not generated in {output_dir}"

    # Validate outputted discovery manifest
    output_yaml = yaml_files[0]
    extra_keys, missing_keys, mismatched_values = compare_yaml_keys_and_values(
        input_yaml, output_yaml)

    assert not extra_keys, (
    "Extra keys in output YAML:\n" +
    "\n".join(f"  {key}" for key in sorted(extra_keys))
    )
    assert not missing_keys, (
    "Missing keys in output YAML:\n" +
    "\n".join(f"  {key}" for key in sorted(missing_keys))
    )
    assert not mismatched_values, (
    "Mismatched values:\n" +
    "\n".join(
        f"  {key}:\n    input:  {v['input']}\n    output: {v['output']}"
        for key, v in sorted(mismatched_values.items())
    ))
