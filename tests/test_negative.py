import subprocess

from utils.command import build_analysis_command
from utils.common import run_containerless_parametrize


@run_containerless_parametrize
def test_analysis_wrong_target(analysis_data, additional_args):
    application_data = analysis_data['jee_example_app']

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        "some_wrong_target",
        **additional_args
    )

    process = subprocess.run(
        command,
        shell=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'
    )

    assert process.returncode != 0

    assert 'Error: unknown target:' in process.stderr
