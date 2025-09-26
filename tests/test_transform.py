import json
import os
import shutil
import subprocess
import zipfile

import pytest
import yaml
from jsonschema.exceptions import ValidationError

from utils import constants
from jsonschema import validate


# Polarion TC 376
@pytest.mark.parametrize('transformation_name', json.load(open("data/openrewrite_transformation.json")))
def test_transform_code_with_openrewrite(transformation_name, openrewrite_transformation_data):
    application_data = openrewrite_transformation_data[transformation_name]
    kantra_path = os.getenv(constants.KANTRA_CLI_PATH)
    extraction_path = os.getenv(constants.REPORT_OUTPUT_PATH)

    shutil.rmtree(extraction_path)

    application_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/applications', application_data['file_name'])
    extracted_app_path = os.path.join(os.getenv(constants.REPORT_OUTPUT_PATH), application_data['app_name'])

    with zipfile.ZipFile(application_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)

    command = f"{kantra_path} transform openrewrite --input {extracted_app_path} --target {application_data['targets']}"

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout
    assert 'BUILD SUCCESS' in output, "Failed command is: " + command

    with open(
            os.path.join(extracted_app_path, application_data['assertion_file']), 'r'
    ) as file:
        file_data = file.read()

    assert application_data['assertion'] in file_data


