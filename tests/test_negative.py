import subprocess

from utils.command import build_analysis_command


def test_analysis_wrong_target(analysis_data):
    application_data = analysis_data['jee_example_app']

    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        "some_wrong_target"
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

    assert 'failed to load provider settings open /opt/output/output.yaml: no such file or directory' in process.stderr
