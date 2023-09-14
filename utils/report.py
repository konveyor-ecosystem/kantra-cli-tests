import json
import os

from utils import constants

def assert_story_points_from_report_file(**kwargs):
    """
    Asserts that the story points value in the report file is a number >= 0

    Args:
        **kwargs: Optional keyword arguments.
            report_path (str): The path to the report file. If not provided,
                the function will use the value of the 'REPORT_OUTPUT_PATH' environment variable.

    Raises:
        AssertionError: If the story points in the report file do not match the provided value.

    Returns:
        None.

    """
    report_path = os.getenv(constants.REPORT_OUTPUT_PATH)
    report_path = kwargs.get('report_path', report_path)

    with open(report_path + "/api/applications.json") as file:
        json_data = json.load(file)

    assert json_data[0]['storyPoints'] >= 0
