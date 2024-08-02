import os
import tempfile
import zipfile
from contextlib import contextmanager

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
