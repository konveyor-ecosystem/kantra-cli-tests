import os
import shutil
import subprocess
import zipfile

import yaml
from jsonschema.exceptions import ValidationError

from utils import constants
from jsonschema import validate


# Polarion TC 376
def test_transform_xml_rules_to_yaml():
    kantra_path = os.getenv(constants.KANTRA_CLI_PATH)
    custom_rule_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/xml', 'javax-package-custom.windup.xml')
    output_path = os.getenv(constants.REPORT_OUTPUT_PATH)

    command = f"{kantra_path} transform rules --input {custom_rule_path} --output {output_path}"

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout
    yaml_path = output_path + "/01-javax-package-custom/javax-package-custom.windup.yaml"

    assert os.path.exists(yaml_path)
    with open(yaml_path) as file:
        yaml_rule = file.read()

    assert 'javax-package-00001' in yaml_rule

    try:
        validate(
            yaml.load(yaml_rule, Loader=yaml.FullLoader),
            yaml.load(constants.CUSTOM_RULE_YAML_SCHEMA, Loader=yaml.FullLoader)
        )
    except ValidationError as e:
        assert True is False, 'The validation of the generated YAML rule failed. ' + e.message


# Polarion TC 376
def test_transform_code_with_openrewrite():
    kantra_path = os.getenv(constants.KANTRA_CLI_PATH)
    complete_duke_app_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/applications', 'complete-duke.zip')
    extraction_path = os.getenv(constants.REPORT_OUTPUT_PATH)
    extracted_app_path = os.path.join(os.getenv(constants.REPORT_OUTPUT_PATH), 'complete-duke')

    with zipfile.ZipFile(complete_duke_app_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)

    command = f"{kantra_path} transform openrewrite --input {extracted_app_path} --target jakarta-imports"

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout
    assert 'BUILD SUCCESS' in output

    with open(
            os.path.join(extracted_app_path, 'src/main/java/eu/agilejava/dukes/greeting/DukesRepository.java'), 'r'
    ) as file:
        file_data = file.read()

    assert 'import jakarta' in file_data, 'Jakarta imports not found in the file'

    shutil.rmtree(extracted_app_path)

