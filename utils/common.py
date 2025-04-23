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

def verify_triggered_rule(report_data, rule_id: str):
    ruleset = next((item for item in report_data['rulesets'] if rule_id in item.get('violations', {})), None)

    assert ruleset is not None, "Ruleset property not found in output"
    assert len(ruleset.get('skipped', [])) == 0, "Custom Rule was skipped"
    assert len(ruleset.get('unmatched', [])) == 0, "Custom Rule was unmatched"
    assert 'violations' in ruleset, "Custom rules didn't trigger any violation"
    assert rule_id in ruleset['violations'], "The test rule triggered no violations"