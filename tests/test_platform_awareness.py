import re
import subprocess
import yaml

from utils import constants
from utils.command import build_pa_discovery_command

# Polarion TC MTA-617
def test_cloudfoundry_local_discovery():
    input_yaml = './data/yaml/asset_generation/cf-nodejs-app.yaml'
    output_yaml = '.tmp/discovery.yaml'

    command = build_pa_discovery_command(input_yaml,
        **{'output-dir': output_yaml}
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE,
        encoding='utf-8').stdout
    
    result = compare_yaml_keys(input_yaml, output_yaml)

    print("Extra keys in output YAML:")
    for key in sorted(result["extra_keys_in_output"]):
        print("  ", key)

    print("\nMissing keys in output YAML:")
    for key in sorted(result["missing_keys_in_output"]):
        print("  ", key)

def normalize_key(key):
    """Normalize keys by lowercasing and removing non-alphanumeric characters to loosely match keys."""
    return re.sub(r'[^a-z0-9]', '', key.lower())

def extract_keys(d, parent_key=''):
    """
    Recursively extract keys from nested dicts.
    Returns a set of normalized keys with their full path (dot separated).
    """
    keys = set()
    if isinstance(d, dict):
        for k, v in d.items():
            norm_k = normalize_key(k)
            full_key = f"{parent_key}.{norm_k}" if parent_key else norm_k
            keys.add(full_key)
            keys.update(extract_keys(v, full_key))
    elif isinstance(d, list):
        for item in d:
            keys.update(extract_keys(item, parent_key))
    return keys

def compare_yaml_keys(input_yaml_str, output_yaml_str):
    input_data = yaml.safe_load(input_yaml_str)
    output_data = yaml.safe_load(output_yaml_str)

    input_keys = extract_keys(input_data)
    output_keys = extract_keys(output_data)

    extra_keys = output_keys - input_keys
    missing_keys = input_keys - output_keys

    return {
        "extra_keys_in_output": extra_keys,
        "missing_keys_in_output": missing_keys
    }

