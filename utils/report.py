import json
import os
import shutil

import yaml
from bs4 import BeautifulSoup

from utils import constants


def get_json_from_report_output_js_file(return_first = True, **kwargs):
    """
        Loads and returns a JSON from the output.js file of the report

        Args:
            return_first: flag to return only first value (default). If false - will return array of values instead.
            **kwargs: Optional keyword arguments.
                report_path (str): The path to the report file. If not provided,
                    the function will use the value of the 'REPORT_OUTPUT_PATH' environment variable.

        Returns:
            JSON data

        """
    report_path = os.getenv(constants.REPORT_OUTPUT_PATH)
    report_path = kwargs.get('report_path', report_path)

    with open(os.path.join(report_path, "static-report", "output.js"), encoding='utf-8') as file:
        js_report = file.read()
    if return_first:
        return json.loads(js_report.split('window["apps"] = ')[1])[0]
    else:
        return json.loads(js_report.split('window["apps"] = ')[1])

def get_dict_from_output_yaml_file(filename = "output.yaml", **kwargs):
    """
        Loads and returns a JSON from the output.js file of the report

        Args:
            filename: Which filename should be used. Useful in case of bulk analysis as filename can differ
            **kwargs: Optional keyword arguments.
                report_path (str): The path to the report file. If not provided,
                    the function will use the value of the 'REPORT_OUTPUT_PATH' environment variable.

        Returns:
            JSON data

        """

    report_path = os.getenv(constants.REPORT_OUTPUT_PATH)
    report_path = kwargs.get('report_path', report_path)

    with open(os.path.join(report_path, filename), encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    return data


def assert_non_empty_report(report_path):
    """
    Asserts that the story points value in the report file is a number >= 0

    Args:
        report_path (str): The path to the report file. If not provided,
        the function will use the value of the 'REPORT_OUTPUT_PATH' environment variable.

    Raises:
        AssertionError: If the report looks empty or is missing.

    Returns:
        None.

    """
    report_data = get_json_from_report_output_js_file(report_path=report_path)

    some_incidents = False

    for rule in report_data['rulesets']:
        violations = rule.get('violations', {})

        for violation in violations.values():
            if 'incidents' in violation:
                some_incidents = True
                break

    assert os.path.exists(os.path.join(report_path, "static-report", "index.html")), "Missing index.html file in static-report under " + report_path
    assert some_incidents, "Missing incidents in static-report js data file"


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
    report_data = get_json_from_report_output_js_file()

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
        AssertionError: If the Insights occurence count in the report file is < 0.

    Returns:
        None.

    """
    report_data = get_dict_from_output_yaml_file()

    occurrences = -1
    for rule in report_data['rulesets']:
        insights = rule.get('insights', {})

        for insight in insights.values():
            if 'incidents' in insight:
                if occurrences == -1:
                    occurrences = 0
                occurrences += len(insight['incidents'])

    assert occurrences > 0, "No insights were generated"

def clearReportDir():
    report_path = os.getenv(constants.REPORT_OUTPUT_PATH)

    # Check that path exists and it is a dir
    if report_path and os.path.exists(report_path) and os.path.isdir(report_path):
        # Cleaning up dir's content
        for filename in os.listdir(report_path):
            file_path = os.path.join(report_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Could not remove content of {file_path}. Error: {e}')
    else:
        print(f'Path {report_path} does not exist or is not a directory')