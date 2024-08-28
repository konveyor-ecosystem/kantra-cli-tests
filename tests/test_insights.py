import os
import subprocess

from utils import constants
from utils.command import build_analysis_command
from utils.report import assert_insights_from_report_file

# Polarion TC 598
def test_insights_binary_app(analysis_data):
    application_data = analysis_data['jee_example_app']
    custom_rule_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/xml', 'weblogic-custom.windup.yaml')

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target']
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' in output
    assert_insights_from_report_file()

# Polarion TC 374
def test_custom_rules(analysis_data):
    application_data = analysis_data['tackle-testapp-project']
    custom_rule_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/yaml', 'custom_rule_insights.yaml')

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{'rules': custom_rule_path}
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' in output
    report_data = get_json_from_report_output_file()

    for rule in report_data['rulesets']:
        insights = rule.get('insights', {})

        for insight in insights.values():
            if rule['name'] == 'custom-ruleset':
                if insight['description'] == 'Properties file (Insights TC0)':
                    assert(insight['labels'][1], 'tag=Properties File (Insights TC0)')
                elif insight['description'] == 'Properties file (Insights TC1)':
                    assert(insight['labels'][1], 'tag=Properties File (Insights TC1)')
                elif insight['description'] == 'Properties file (Insights TC2)':
                    assert(insight['incidents'][0]['message'], 'Found properties file ruleID discover-properties-file-TC2')
