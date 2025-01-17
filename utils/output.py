import os
import yaml

from utils import constants


def assert_analysis_output_violations(expected_output_dir, initialize_if_empty = True):
    """
    Asserts that the Violations (Issues) and their Incidents from analysis output

    Raises:
        AssertionError: If analysis output (violations&incidents) were different.

    Returns:
        None.

    """

    expected_output, expected_output_path = dict(), os.path.join(expected_output_dir, "output.yaml")
    got_output, got_output_path = get_dict_from_output_file("output.yaml")
    got_output = normalize_output(got_output)

    if not os.path.exists(expected_output_dir):
        os.mkdir(expected_output_dir)

    if not os.path.exists(expected_output_path):
        with open(expected_output_path, 'w') as f:
            yaml.dump(got_output, f)

        assert False, "Expected output file '%s' did not exist, initializing it with the current test output" % expected_output_path

    else:
        with open(expected_output_path) as f:
            expected_output = yaml.safe_load(f)

    assert got_output == expected_output, "Got different analysis output, diff: \n%s" % get_files_diff(expected_output_path, got_output_path)


def assert_analysis_output_dependencies(expected_output_dir):
    """
    Asserts that the Dependencies from analysis output

    Raises:
        AssertionError: If dependencies were different.

    Returns:
        None.

    """

    expected_output, expected_output_path = dict(), os.path.join(expected_output_dir, "dependencies.yaml")
    got_output, got_output_path = get_dict_from_output_file("dependencies.yaml")

    if not os.path.exists(expected_output_path):
        with open(expected_output_path, 'w') as f:
            yaml.dump(got_output, f)

        assert False, "Expected dependencies file '%s' did not exist, initializing it with the current test output" % expected_output_path

    else:
        with open(expected_output_path) as f:
            expected_output = yaml.safe_load(f)

    assert got_output == expected_output, "Got different dependencies output, diff: \n%s" % get_files_diff(expected_output_path, got_output_path)


def get_dict_from_output_file(filename, **kwargs):
    """
        Loads and returns a YAML from analysis output Violation file output.yaml

        Returns:
            dict (from YAML file data)

        """
    report_path = os.getenv(constants.REPORT_OUTPUT_PATH)
    report_path = kwargs.get('report_path', report_path)
    output_path = os.path.join(report_path, filename)

    with open(output_path, encoding='utf-8') as file:
        return yaml.safe_load(file), output_path


def normalize_output(rulesets: dict):
    """
        Does a pruning on output file to delete not used fields (skipped and unmatched rules),
        makes incident paths generic to allow compare container and container-less results.

        Structure: ruleset -> rules -> rule violation -> incidents
    """
    for ruleset in rulesets:
        if ruleset.get('unmatched'):
            del ruleset['unmatched']
        if ruleset.get('skipped'):
            del ruleset['skipped']
        #del ruleset['insights'] # This is for tags, maybe keep them?

        # TODO: incidents path make compatible container with containerless

    return ruleset

def get_files_diff(a, b):
    # TODO: do something better
    return os.popen("diff '%s' '%s'" % (a, b)).read()
