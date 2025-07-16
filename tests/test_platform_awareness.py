import os
import subprocess
import pytest

from utils import constants
from utils.command import build_pa_discovery_command

# Polarion TC MTA-617
def test_cloudfoundry_local_discovery():
    input_yaml = './data/yaml/asset_generation/cf-nodejs-app.yaml'
    output_yaml = '.tmp/discovery.yaml'

    command = build_pa_discovery_command(input_yaml,
        **{'output-dir': output_yaml}
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE,
        encoding='utf-8').stdout

