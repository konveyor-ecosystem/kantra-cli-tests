import json
import os

from bs4 import BeautifulSoup

from utils import constants


def get_json_from_report_output_file(**kwargs):
    """
        Loads and returns a JSON from the output.js file of the report

        Args:
            **kwargs: Optional keyword arguments.
                report_path (str): The path to the report file. If not provided,
                    the function will use the value of the 'REPORT_OUTPUT_PATH' environment variable.

        Returns:
            JSON data

        """
    report_path = os.getenv(constants.REPORT_OUTPUT_PATH)
    report_path = kwargs.get('report_path', report_path)

    with open(report_path + "/static-report/output.js", encoding='utf-8') as file:
        js_report = file.read()
    return json.loads(js_report.split('window["apps"] = ')[1])[0]


def assert_story_points_from_report_file():
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
    report_data = get_json_from_report_output_file()

    story_points = -1
    for rule in report_data['rulesets']:
        violations = rule.get('violations', {})

        for violation in violations.values():
            if 'incidents' in violation and 'effort' in violation:
                if story_points == -1:
                    story_points = 0
                story_points += len(violation['incidents']) * violation['effort']

    assert story_points >= 0, "Non valid value found in Story Points from Report: " + str(story_points)

def assert_insights_from_report_file():
    """
    Asserts that the Insights occurrence count in the report file is > 0.
 
    Args:
        **kwargs: Optional keyword arguments.
            report_path (str): The path to the report file. If not provided,
                the function will use the value of the 'REPORT_OUTPUT_PATH' environment variable.
 
    Raises:
        AssertionError: If the story points in the report file do not match the provided value.
 
    Returns:
        None.
 
    """
    report_data = get_json_from_report_output_file()
 
    occurrences = -1
    for rule in report_data['rulesets']:
        insights = rule.get('insights', {})
 
        for insight in insights.values():
            if 'incidents' in insight:
                if occurrences == -1:
                    occurrences = 0
                occurrences += len(insight['incidents'])
 
    assert occurrences >= 0, "Invalid value found for Insights occurrences in Report: " + str(occurrences)
