import os
import subprocess
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
