import argparse
import re
import unittest

import re
import json
import unittest
import sys
import os
from unittest.runner import TextTestResult


NUMBER_OF_TASKS_FOR_ASSIGNMENT = 6


class CustomTestResult(TextTestResult):
    """
    Custom test result class to handle the output format for Ed.

    The only difference with the default TextTestResult is that it stores the test results
    in a list instead of printing them to the console.
    This allows us to return the results in JSON format for Ed.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_results = []

    def addSuccess(self, test):
        self._record_result(test, True, "Well done")

    def addFailure(self, test, err):
        message = self._exc_info_to_string(err, test)
        self._record_result(test, False, message)

    def addError(self, test, err):
        message = self._exc_info_to_string(err, test)
        self._record_result(test, False, message, ok=False)

    def _record_result(self, test, passed, feedback, ok=True):
        docstring = test._testMethodDoc or ""
        
        task_number_match = re.search(r"[Tt]ask(\d+)", str(test), re.DOTALL)
        name_match = re.search(r"#name\((.*?)\)", docstring, re.DOTALL)

        # Test name like this: "Task 1: Test the cool function number 3"
        test_name_prefix = f"{'Task ' + task_number_match.group(1) if task_number_match else "General"}: "
        test_name = f"{test_name_prefix}{name_match.group(1).strip() if name_match else test._testMethodName}"

        score_match = re.search(r"#score\((\d+)\)", docstring, re.DOTALL)
        hidden_test = re.search(r"#hidden", docstring, re.DOTALL)
        private_test = re.search(r"#private", docstring, re.DOTALL)
        
        result = {
            "name": test_name,
            "score": 0 if not passed else (int(score_match.group(1)) if score_match else 1),
            "ok": ok,
            "passed": passed,
            "feedback": feedback.strip(),
            "hidden": bool(hidden_test),
            "private": bool(private_test),
        }
        self.test_results.append(result)
            

def get_matching_files(regex_pattern):
    """
    Return all files in the "tests" directory matching the regex pattern.
    :param regex_pattern: The regex pattern to match test files.
    """
    test_dir = "tests"
    all_files = os.listdir(test_dir)
    # Get all files, sort them to ensure the order is consistent
    return list(sorted([os.path.join(test_dir, f) for f in all_files if re.fullmatch(regex_pattern, f)]))


def run_tests(file_pattern, running_in_ed=False):
    """
    Run all test files inside the "tests" directory matching the file pattern.

    :param file_pattern: The regex pattern to match test files inside the "tests" directory.
    :param running_in_ed: If True, run tests in Ed mode, meaning suppressing output and using a custom result class.
    :return: A dictionary with the test results in Ed format if running_in_ed is True, otherwise None.
    """
    if not file_pattern:
        print("No file pattern provided. This is required to ensure only 'graded' tests are run.")
        sys.exit(1)
    
    # Get all test files matching the pattern, rename them to the format expected by unittest
    test_files = [test_file.replace(".py", "").replace("/", ".") for test_file in get_matching_files(file_pattern)]

    if not test_files:
        print("No matching test files found.")
        sys.exit(1)
    
    
    loader = unittest.TestLoader()
    
    if running_in_ed:
        # If we are running in Ed, set buffer=True to avoid getting student's prints out in the console
        runner = unittest.TextTestRunner(resultclass=CustomTestResult, verbosity=0, buffer=True)
        
        # Run all files, save the result in a list
        all_results = []
        for test_file in test_files:
            suite = loader.loadTestsFromName(test_file)
            result = runner.run(suite)
            all_results.extend(result.test_results)

        ed_output = {
            "testcases": all_results,
        }
        return ed_output
    else:
        # If we are running locally, set verbosity=1 to get the test results printed and use the default result class
        runner = unittest.TextTestRunner(verbosity=1)

        # Run all files, print the result in the console
        for test_file in test_files:
            print("\n\n\033[1m\033[94m" + f"Running {test_file}..." + "\033[0m")
            print("----------------------------------------------------------------------")
            suite = loader.loadTestsFromName(test_file)
            result = runner.run(suite)
        
        return None


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "task",
        help=(
            "The task number you'd like to run. "
            "Leave blank for all tasks.\n\n"
            "Example: run_tests.py 3\n"
            "Runs the tests in test_task3.py file."
        ),
        default="",
        nargs="?",
    )
    p.add_argument(
        "--ed",
        action="store_true",
        help="Run tests on Ed.",
    )
    
    args = p.parse_args()

    task_number = args.task
    
    if args.ed:
        # If running in Ed, we want to run all tests - input task number should be ignored.
        task_number = None
    else:
        # If not running in Ed, ask user for a task number if they haven't provided one
        if task_number == '':
            task_number = input(f"Enter task [1 - {NUMBER_OF_TASKS_FOR_ASSIGNMENT}], leave blank to run all tests: ")
        
        # Try to convert task_number to an integer. If it fails, set it to None to run all tasks
        try:
            task_number = int(task_number)
        except ValueError:
            task_number = None
            
    # If a valid task number is provided after the process above, only run that file. Otherwise, run all files.
    if task_number is not None:
        file_pattern = rf"^test_task{task_number}\.py$"
    else:
        file_pattern = rf"^test_task[1-{NUMBER_OF_TASKS_FOR_ASSIGNMENT}]\.py$"

    output = run_tests(file_pattern=file_pattern, running_in_ed=args.ed)
    
    # If we are running in Ed, we want to print the output in JSON format. Otherwise, the tests will print the results.
    if args.ed:
        print(json.dumps(output, indent=2))
