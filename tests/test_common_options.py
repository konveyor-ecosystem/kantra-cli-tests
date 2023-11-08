import os
import subprocess

from utils import constants


# Polarion TC MTA-372
def test_list_targets():
    kantra_path = os.getenv(constants.KANTRA_CLI_PATH)
    command = kantra_path + ' analyze --list-targets'

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    for i in ['hibernate-search5', 'eap', 'azure-appservice', 'openjdk11', 'java-ee7', 'quarkus']:
        assert i in output


# Polarion TC MTA-372
def test_list_sources():
    kantra_path = os.getenv(constants.KANTRA_CLI_PATH)
    command = kantra_path + ' analyze --list-sources'

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    for i in ['log4j', 'eap', 'springboot', 'openjdk11', 'java-ee', 'javaee', 'openshift', 'oraclejdk']:
        assert i in output
