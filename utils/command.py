import os

from utils import constants


def build_analysis_command(binary_name, source, target, is_bulk=False, output_path=None, settings=None, **kwargs):
    """
        Builds a string for executing the "analyze" subcommand

        Args:
            binary_name (str): binary file of the application to be analyzed.
            source (str): Source of the application.
            target (str): Target for the application to migrate to.
            is_bulk (bool): Defines if '--bulk' (true) or `--overwrite`(false) run is performed
            **kwargs (str): Optional keyword arguments to be passed to Kantra as additional options.
                this argument takes a dict, where each key is the argument, which can be passed with or without the '--'

        Returns:
            str: The full command to execute with the specified options and arguments.

        Raises:
            Exception: If `binary_path` is not provided.
    """
    kantra_path = os.getenv(constants.KANTRA_CLI_PATH)

    if output_path:
        report_path = output_path
    else:
        report_path = os.getenv(constants.REPORT_OUTPUT_PATH)

    if not binary_name:
        raise Exception('Binary path is required')

    if is_bulk:
        run_type = '--bulk'
    else:
        run_type = '--overwrite'

    if os.path.isabs(binary_name):
        binary_path = binary_name
    else:
        binary_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/applications', binary_name)

    command = kantra_path + ' analyze ' + run_type + ' --input ' + binary_path + ' --output ' + report_path

    if source:
        command += ' --source ' + source

    if target:
        command += ' --target ' + target

    if settings:
        command += ' --maven-settings ' + settings

    for key, value in kwargs.items():
        if '--' not in key:
            key = '--' + key
        command += ' ' + key

        if value:
            command += ' ' + value

    print(command)
    return command
