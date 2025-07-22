import os
import platform
import tempfile
import zipfile
from contextlib import contextmanager

import pytest
from functools import wraps

from utils import constants


@contextmanager
def extract_zip_to_temp_dir(application_path):
    """
    Creates a temporary directory and extracts a zip file to it.

    :param application_path: Path to the zip file
    :yield: path to the extracted zip file
    """

    tempdir = tempfile.TemporaryDirectory(dir=os.getenv(constants.PROJECT_PATH))

    # Adjusts the permissions to allow access to subprocesses
    os.chmod(tempdir.name, 0o777)

    with zipfile.ZipFile(application_path, 'r') as zip_ref:
        zip_ref.extractall(tempdir.name)

    yield tempdir.name

def run_containerless_parametrize(func):
    args_list = [{"--run-local=true": None}]  # Always include local mode

    if platform.system().lower() != "windows":
        args_list.append({"--run-local=false": None})  # Add container mode only if not Windows

    @pytest.mark.parametrize(
        "additional_args",
        args_list,
        ids=lambda args: list(args)[0]  # More readable way
    )
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

def verify_triggered_rules(report_data, rule_id_list, expected_unmatched_rules = False):
    """

    Args:
        report_data: Report data that includes rulesets
        rule_id_list: List of actual rule IDs we are looking for
        expected_unmatched_rules: Sometimes rulesets can include unmatched rules (on purpose) so expected_unmatched_rules was added to avoid failure

    Returns:

    """

    errors = []
    for rule_id in rule_id_list:
        # print(f"Checking rule: {rule_id}")
        ruleset = next((item for item in report_data['rulesets'] if rule_id in item.get('violations', {})), None)

        if ruleset is None:
            errors.append(f"Error for rule ID '{rule_id}': Ruleset property not found in output.")
            continue # Move to the next rule if the ruleset isn't found

        if len(ruleset.get('skipped', [])) != 0:
            errors.append(f"Error for rule ID '{rule_id}': Custom Rule was skipped. Skipped rules: {ruleset.get('skipped', [])}")

        if len(ruleset.get('unmatched', [])) != 0 and not expected_unmatched_rules:
            errors.append(f"Error for rule ID '{rule_id}': Custom Rule was unmatched. Unmatched rules: {ruleset.get('unmatched', [])}. Expected unmatched: {expected_unmatched_rules}")

        if 'violations' not in ruleset:
            errors.append(f"Error for rule ID '{rule_id}': Custom rules didn't trigger any violation.")
        elif rule_id not in ruleset['violations']:
            errors.append(f"Error for rule ID '{rule_id}': The test rule triggered no violations for this specific rule ID.")

    if errors:
        error_message = "The following rule validation errors occurred:\n" + "\n".join(errors)
        print(f"Failed assertions: {error_message}")
        raise AssertionError(error_message)

def extract_rules(analysis: dict) -> list[str]:
    return [issue.get("rule") for issue in analysis.get("issues", []) if issue.get("rule")]


def verify_triggered_yaml_rules(report_data, rule_id_list, expected_unmatched_rules = False):
    """

        Args:
            report_data: Report data that includes rulesets
            rule_id_list: List of actual rule IDs we are looking for
            expected_unmatched_rules: Sometimes rulesets can include unmatched rules (on purpose) so expected_unmatched_rules was added to avoid failure

        Returns:

        """

    errors = []

    for rule_id in rule_id_list:
        # Find the ruleset that contains this rule ID in its 'violations'
        ruleset = next((item for item in report_data if rule_id in item.get('violations', {})), None)

        if ruleset is None:
            errors.append(f"Error for rule ID '{rule_id}': Ruleset property not found in output.")
            continue  # Move to the next rule if the ruleset isn't found

        if len(ruleset.get('skipped', [])) != 0:
            errors.append(f"Error for rule ID '{rule_id}': Custom Rule was skipped. Skipped rules: {ruleset.get('skipped', [])}")

        if len(ruleset.get('unmatched', [])) != 0 and not expected_unmatched_rules:
            errors.append(f"Error for rule ID '{rule_id}': Custom Rule was unmatched. Unmatched rules: {ruleset.get('unmatched', [])}. Expected unmatched: {expected_unmatched_rules}")

        if 'violations' not in ruleset:
            errors.append(f"Error for rule ID '{rule_id}': Custom rules didn't trigger any violation.")
        elif rule_id not in ruleset['violations']:
            errors.append(f"Error for rule ID '{rule_id}': The test rule triggered no violations for this specific rule ID.")

    if errors:
        error_message = "The following rule validation errors occurred:\n" + "\n".join(errors)
        print(f"Failed assertions: {error_message}")
        raise AssertionError(error_message)

def extract_name_and_violations_from_dictionary(data):
    result = {}
    for item in data:
        if not item.get("violations") and not item.get("insights"):
            continue
        item.pop("unmatched", None)
        name = item.get("name")
        if name is not None:
            result[name] = item.get("violations", [])
    return result