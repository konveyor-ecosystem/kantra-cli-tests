import re
import yaml

def normalize_key(key):
    return re.sub(r'[^a-z0-9]', '', key.lower())

def extract_keys_and_values(d, parent_key=''):
    """
    Recursively extract keys and values from nested dicts and lists.
    Returns a dictionary mapping normalized full keys to values.
    """
    result = {}
    if isinstance(d, dict):
        for k, v in d.items():
            norm_k = normalize_key(k)
            full_key = f"{parent_key}.{norm_k}" if parent_key else norm_k
            if isinstance(v, (dict, list)):
                result.update(extract_keys_and_values(v, full_key))
            else:
                result[full_key] = v
    elif isinstance(d, list):
        for idx, item in enumerate(d):
            # For lists, treat index as part of the key to avoid flattening ambiguity
            result.update(extract_keys_and_values(item, f"{parent_key}[{idx}]"))
    return result

def compare_yaml_keys_and_values(input_yaml, output_yaml):
    with open(input_yaml, 'r') as f:
        input_data = yaml.safe_load(f)
    with open(output_yaml, 'r') as f:
        output_data = yaml.safe_load(f)

    input_map = extract_keys_and_values(input_data)
    output_map = extract_keys_and_values(output_data)

    input_keys = set(input_map.keys())
    output_keys = set(output_map.keys())

    extra_keys = output_keys - input_keys
    missing_keys = input_keys - output_keys
    common_keys = input_keys & output_keys

    # Value mismatches
    mismatched_values = {
        key: {'input': input_map[key], 'output': output_map[key]}
        for key in common_keys
        if input_map[key] != output_map[key]
    }

    return {
        'extra_keys_in_output': extra_keys,
        'missing_keys_in_output': missing_keys,
        'mismatched_values': mismatched_values
    }
