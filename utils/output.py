import os
import yaml

from utils import constants


def assert_analysis_output_violations(expected_output_dir, output_dir, input_root_path = None):
    """
    Asserts that the Violations (Issues) and their Incidents from analysis output

    Raises:
        AssertionError: If analysis output (violations&incidents) were different.

    Returns:
        None.

    """

    expected_output, expected_output_path = dict(), os.path.join(expected_output_dir, "output.yaml")
    got_output, got_output_path = get_dict_from_output_file("output.yaml", dir=output_dir)
    got_output_normalized_path = got_output_path + ".normalized"
    # create a preprocessed/normalized outfile file to allow its comparision across platforms and setups
    with open(got_output_normalized_path, 'w') as f:
            yaml.dump(normalize_output(got_output, input_root_path), f)
    with open(got_output_normalized_path, encoding='utf-8') as file:
        got_output = yaml.safe_load(file)

    if not os.path.exists(expected_output_dir):
        os.mkdir(expected_output_dir)

    if not os.path.exists(expected_output_path):
        with open(expected_output_path, 'w') as f:
            yaml.dump(got_output, f)

        assert False, "Expected output file '%s' did not exist, initializing it with the current test output" % got_output_normalized_path

    else:
        with open(expected_output_path) as f:
            expected_output = yaml.safe_load(f)

    assert got_output == expected_output, "Got different analysis output, diff: \n%s" % get_files_diff(expected_output_path, got_output_normalized_path)


def assert_analysis_output_dependencies(expected_output_dir, output_dir):
    """
    Asserts that the Dependencies from analysis output

    Raises:
        AssertionError: If dependencies were different.

    Returns:
        None.

    """

    expected_output, expected_output_path = dict(), os.path.join(expected_output_dir, "dependencies.yaml")
    got_output, got_output_path = get_dict_from_output_file("dependencies.yaml", dir=output_dir)

    if not os.path.exists(expected_output_path):
        with open(expected_output_path, 'w') as f:
            yaml.dump(got_output, f)

        assert False, "Expected dependencies file '%s' did not exist, initializing it with the current test output" % expected_output_path

    else:
        with open(expected_output_path) as f:
            expected_output = yaml.safe_load(f)

    assert got_output == expected_output, "Got different dependencies output, diff: \n%s" % get_files_diff(expected_output_path, got_output_path)


def get_dict_from_output_file(filename, dir=None, **kwargs):
    """
        Loads and returns a YAML from analysis output Violation file output.yaml, TODO dir cleaner

        Returns:
            dict (from YAML file data)

        """
    report_path = os.getenv(constants.REPORT_OUTPUT_PATH)
    report_path = kwargs.get('report_path', report_path)
    if dir:
        report_path = dir
    output_path = os.path.join(report_path, filename)

    with open(output_path, encoding='utf-8') as file:
        return yaml.safe_load(file), output_path


def normalize_output(rulesets: dict, input_root_path):
    """
        Does a pruning on output file to delete not used fields (skipped and unmatched rules),
        makes incident paths generic to allow compare container and container-less results.
    """
    for ruleset in rulesets:
        if ruleset.get('unmatched'):
            del ruleset['unmatched']
        if ruleset.get('skipped'):
            del ruleset['skipped']
        if ruleset.get('insights'):
            del ruleset['insights']

        if ruleset.get('violations'):
            for rulename in ruleset['violations']:
                violation = ruleset.get('violations').get(rulename)
                if violation:
                    for incident in violation.get('incidents'):
                        incident['uri'] = trim_incident_uri(incident['uri'], input_root_path)    # Normalize incidents path to make compatible container with containerless, fix slashes, etc.

    # delete not matched ruleset
    rulesets = [ruleset for ruleset in rulesets if ruleset.get('violations') or ruleset.get('tags')]

    return rulesets

def get_files_diff(a, b):
    return os.popen("diff -u '%s' '%s'" % (a, b)).read()

def trim_incident_uri(uri, input_root_path):
    uri = uri.replace(input_root_path, "")  # remove containerless test input prefix path

    uri = uri.replace("\\", "/")   # replace windows back-slashes with unix slashes
    uri = uri.replace("file:////", "file:///")    # ensure windows&unix mixture will not produce invalid file protocol prefix
    uri = uri.replace("file:///opt/input/source/", "") # remove container analysis input mount prefix, TODO: file:///root/.m2, etc

    # Ensure paths are relative
    uri = uri.replace("file:///", "")    # ensure windows&unix mixture will not produce invalid file protocol prefix

    # Remove all path prefix to java-project if present
    if 'java-project' in uri:
       uri = uri.split('java-project')[-1]

    return uri
