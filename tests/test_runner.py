#!/usr/bin/env python3
"""
Test runner script for RoadFlow API services.
This script can be used to run specific test suites or all tests.
"""

import subprocess
import sys
from pathlib import Path


def run_tests(test_path=None, verbose=True, coverage=False):
    """
    Run tests using pytest.
    
    Args:
        test_path: Specific test file or directory to run
        verbose: Enable verbose output
        coverage: Enable coverage reporting
    """
    cmd = ["uv", "run", "pytest"]

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(["--cov=services", "--cov-report=term-missing"])

    if test_path:
        cmd.append(str(test_path))

    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
        return result.returncode
    except KeyboardInterrupt:
        print("\nTest run interrupted by user")
        return 1
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


def main():
    """Main entry point for test runner."""
    import argparse

    parser = argparse.ArgumentParser(description="Run RoadFlow API tests")
    parser.add_argument("path", nargs="?", help="Specific test file or directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-c", "--coverage", action="store_true", help="Enable coverage")
    parser.add_argument("--agents", action="store_true", help="Run only agent tests")
    parser.add_argument("--workflows", action="store_true", help="Run only workflow tests")
    parser.add_argument("--services", action="store_true", help="Run only service tests")

    args = parser.parse_args()

    test_path = None
    if args.path:
        test_path = args.path
    elif args.agents:
        test_path = "tests/services/agents/"
    elif args.workflows:
        test_path = "tests/services/workflows/"
    elif args.services:
        test_path = "tests/services/"

    exit_code = run_tests(test_path, args.verbose, args.coverage)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
