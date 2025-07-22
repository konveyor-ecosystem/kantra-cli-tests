import os
import subprocess

from deepdiff import DeepDiff

from utils import constants
from utils.command import build_analysis_command
from utils.output import normalize_output
from utils.report import assert_story_points_from_report_file, get_dict_from_output_yaml_file


def test_book_server_analysis(book_server_data):
    application_data = book_server_data
    reference_data_path = os.path.join(
        os.getenv(constants.PROJECT_PATH),
        "data", "ci", "shared_tests", "analysis_book-server"
    )

    command = build_analysis_command(
        application_data['filename'],
        application_data['sources'],
        application_data['targets']
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' in output.lower()
    assert_story_points_from_report_file()

    # Parsing report and reference
    report_data = normalize_output(
        get_dict_from_output_yaml_file(),
        os.path.join(os.getenv(constants.PROJECT_PATH), 'data', 'applications', application_data['filename'])
    )
    reference_data = get_dict_from_output_yaml_file(
        filename="output.yaml",
        report_path=reference_data_path
    )

    diff = DeepDiff(report_data, reference_data, ignore_order=True)
    errors = []
    if len(report_data) != len(reference_data):
        report_names = [item.get('name', f"Unnamed_Index_{i}") for i, item in enumerate(report_data) if
                        isinstance(item, dict)]
        reference_names = [item.get('name', f"Unnamed_Index_{i}") for i, item in enumerate(reference_data) if
                           isinstance(item, dict)]

        errors.append(
            f"Mismatch in reports length:\n"
            f"\nReport length: {len(report_data)}. "
            f"Found technology names:\n{', '.join(report_names) if report_names else 'None'}\n"
            f"\nReference report length: {len(reference_data)}. "
            f"Found technology names:\n{', '.join(reference_names) if reference_names else 'None'}"
        )
    if diff != {}:
        errors.append(f"Mismatch in name/violations:\n{diff.pretty()}")
    if errors:
        error_message = "The following rule validation errors occurred:\n" + "\n".join(errors)
        print(f"Failed assertions: {error_message}")
        raise AssertionError(error_message)
