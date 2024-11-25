import os
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
    @pytest.mark.parametrize(
        "additional_args",
        [
            {"--run-local=true": None},  # Running without container
            {"--run-local=false": None}  # Running in container mode
        ],
        ids=lambda args: next(iter(args.keys()))  # Customizing output for better readability
    )
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper