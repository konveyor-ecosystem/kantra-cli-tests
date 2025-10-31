#!/usr/bin/env python3
"""
Test Summary Utility

This script reads pytest JSON report and displays test results in a tabular format.
Useful for Jenkins and CI/CD pipelines to get a clear overview of test results.

Usage:
    python utils/test_summary.py [json_report_file]

Example:
    python utils/test_summary.py test-results/report.json
"""

import json
import sys
from tabulate import tabulate
from pathlib import Path


def print_test_summary(json_file='test-results/report.json'):
    """
    Print test results summary in tabular format

    Args:
        json_file (str): Path to the pytest JSON report file
    """
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON report file not found: {json_file}")
        print(f"Make sure to run pytest with --json-report --json-report-file={json_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in report file: {json_file}")
        sys.exit(1)

    # Extract summary information
    summary = data.get('summary', {})
    total = summary.get('total', 0)
    passed = summary.get('passed', 0)
    failed = summary.get('failed', 0)
    skipped = summary.get('skipped', 0)
    error = summary.get('error', 0)

    tests = data.get('tests', [])

    # Print failed test details first if any
    failed_tests = [t for t in tests if t.get('outcome') == 'failed']
    if failed_tests:
        print("\n" + "="*80)
        print("FAILED TEST DETAILS")
        print("="*80 + "\n")

        for test in failed_tests:
            print(f"Test: {test.get('nodeid', 'Unknown')}")
            print(f"Duration: {test.get('duration', 0):.2f}s")

            # Print failure message if available
            call = test.get('call', {})
            longrepr = call.get('longrepr', '')
            if longrepr:
                print(f"Error:\n{longrepr}")

            print("-" * 80 + "\n")

    # Print overall summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    summary_table = [
        ['Total Tests', total],
        ['Passed', passed],
        ['Failed', failed],
        ['Skipped', skipped],
        ['Errors', error],
        ['Success Rate', f"{(passed/total*100):.1f}%" if total > 0 else "N/A"]
    ]

    print(tabulate(summary_table, headers=['Metric', 'Count'], tablefmt='grid'))

    # Print detailed test results
    print("\n" + "="*80)
    print("DETAILED TEST RESULTS")
    print("="*80 + "\n")

    table_data = []

    for test in tests:
        nodeid = test.get('nodeid', 'Unknown')
        outcome = test.get('outcome', 'unknown').upper()
        duration = test.get('duration', 0)

        # Add status emoji for better visibility
        status_icon = {
            'PASSED': '✓',
            'FAILED': '✗',
            'SKIPPED': '⊝',
            'ERROR': '⚠'
        }.get(outcome, '?')

        # Truncate long test names for better display
        if len(nodeid) > 80:
            nodeid = '...' + nodeid[-77:]

        table_data.append([
            status_icon,
            nodeid,
            outcome,
            f"{duration:.2f}s"
        ])

    if table_data:
        print(tabulate(table_data, headers=['', 'Test Name', 'Status', 'Duration'], tablefmt='grid'))
    else:
        print("No test results found in the report.")

    # Return exit code based on test results
    return 0 if failed == 0 and error == 0 else 1


def print_test_summary_compact(json_file='test-results/report.json'):
    """
    Print a compact version of test results (one-line summary + table)

    Args:
        json_file (str): Path to the pytest JSON report file
    """
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON report: {e}")
        sys.exit(1)

    summary = data.get('summary', {})
    total = summary.get('total', 0)
    passed = summary.get('passed', 0)
    failed = summary.get('failed', 0)
    error = summary.get('error', 0)

    # One-line summary
    print(f"\nTest Results: {passed}/{total} passed, {failed} failed")

    # Compact table
    table_data = []
    for test in data.get('tests', []):
        outcome = test.get('outcome', 'unknown').upper()
        status_icon = '✓' if outcome == 'PASSED' else '✗' if outcome == 'FAILED' else '⊝'
        table_data.append([
            status_icon,
            test.get('nodeid', 'Unknown'),
            f"{test.get('duration', 0):.2f}s"
        ])

    print(tabulate(table_data, headers=['', 'Test', 'Time'], tablefmt='simple'))

    return 0 if failed == 0 and error == 0 else 1


if __name__ == '__main__':
    # Default to looking for report in test-results directory
    report_file = 'test-results/report.json'

    # If compact mode is requested
    compact_mode = '--compact' in sys.argv

    # Allow custom report file path from command line
    # Filter out --compact flag to find the actual file path
    args = [arg for arg in sys.argv[1:] if arg != '--compact']
    if args:
        report_file = args[0]

    if compact_mode:
        exit_code = print_test_summary_compact(report_file)
    else:
        exit_code = print_test_summary(report_file)

    sys.exit(exit_code)
