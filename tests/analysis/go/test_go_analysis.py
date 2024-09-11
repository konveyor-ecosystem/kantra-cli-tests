import os
import subprocess

from utils import constants
from utils.command import build_analysis_command
from utils.report import assert_story_points_from_report_file, get_json_from_report_output_file


# Polarion TC MTA-533, MTA-544
def bug_mta_3661_test_go_provider_analysis_with_app(golang_analysis_data):
    application_data = golang_analysis_data['golang_app']
    custom_rules_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/yaml', 'golang-dep-rules.yaml')

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{'provider': "go",
            'rules': custom_rules_path}
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' in output
    assert_story_points_from_report_file()

    report_data = get_json_from_report_output_file()

    ruleset = next((item for item in report_data['rulesets'] if item.get('description') == 'temp ruleset'), None)

    assert ruleset is not None, "Ruleset property not found in output"
    assert len(ruleset.get('skipped', [])) == 0, "Custom Rule was skipped"
    assert len(ruleset.get('unmatched', [])) == 0, "Custom Rule was unmatched"
    assert 'violations' in ruleset, "Custom rules didn't trigger any violation"
    assert 'file-001' in ruleset['violations'], "file-001 triggered no violations"
    assert 'file-002' in ruleset['violations'], "file-002 triggered no violations"

