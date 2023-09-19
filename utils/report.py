import json
import os

from bs4 import BeautifulSoup

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

    with open(report_path + "/static-report/output.js") as file:
        js_report = file.read()
    report_data = json.loads(js_report.split('window["apps"] = ')[1])

    story_points = -1
    for rule in report_data[0]['rulesets']:
        violations = rule.get('violations', {})

        for violation in violations.values():
            if 'incidents' in violation and 'effort' in violation:
                if story_points == -1:
                    story_points = 0
                story_points += len(violation['incidents']) * violation['effort']

    assert story_points >= 0, "Non valid value found in Story Points from Report: " + str(story_points)
