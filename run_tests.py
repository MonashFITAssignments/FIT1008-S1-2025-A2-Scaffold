import argparse
import re
import unittest

import json
import sys
import os
from unittest.runner import TextTestResult


NUMBER_OF_TASKS_FOR_ASSIGNMENT = 6


class SingleTaskTestResult(TextTestResult):
    """
    Custom test result class to handle the output format for Ed.

    The only difference with the default TextTestResult is that it stores the test results
    in a list instead of printing them to the console.
    This allows us to return the results in JSON format for Ed.

    This class is designed to be run on one task's tests at a time.
    If you want to run it on all tasks at once, you will need to modify this to
    use the task number in aggregate results and the hurdle logic.

    Tags available in the docstring for each test:
    #name(test name): The name of the test
    #score(test score): The score for the test
    #hidden: If the test is hidden
    #private: If the test is private
    #approach: If the test is an approach test (used for aggregating results)
    #hurdle: If the test is a hurdle test (if not passed, that task gets 0)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exactly as Ed describes it in the documentation
        self.test_results = []

        # If any hurdle test fails, we want to set the entire task to 0
        self.any_hurdles_failed = False

        # This is to match our rubric. The nested keys will be:
        # "test" / "approach" -> the Ed-formated result dict
        self.aggregate_results = {}
        self._task_number = None

    def addSuccess(self, test):
        self._record_result(test, True, "Well done")

    def addFailure(self, test, err):
        message = self._exc_info_to_string(err, test)
        self._record_result(test, False, message)

    def addError(self, test, err):
        message = self._exc_info_to_string(err, test)
        # Pass ok as True so Ed would still show the total score - it doesn't matter if the student's code
        # errors or returns the wrong result - it's a failed test either way.
        self._record_result(test, False, message, ok=True)

    def _ensure_aggregate_results(self, task_number):
        """
        Ensure the aggregate results dictionary is added.
        """
        if self.aggregate_results:
            # If the aggregate results already added, just make sure the task number
            # matches. Otherwise, we are running the tests for a different task and the
            # aggregate results will be overwritten, and an error should be raised.
            if self._task_number != task_number:
                raise ValueError("Each test file should only have tests for one task.")
            return
        
        # Create the aggregate result for this task
        self.aggregate_results = {
            "tests": {
                "name": f"[Aggregate] Task {task_number} Tests",
                "score": 0,
                "ok": True,
                "passed": True,
                "feedback": "",
                "hidden": False,
                "private": False,
            },
            "approach": {
                "name": f"[Aggregate] Task {task_number} Approach",
                "score": 0,
                "ok": True,
                "passed": True,
                "feedback": "",
                "hidden": False,
                "private": False,
            },
        }

        # And add the object to Ed output - we will be changing it as we go
        self.test_results.append(self.aggregate_results["tests"])
        self.test_results.append(self.aggregate_results["approach"])

        self._task_number = task_number

    def _record_result(self, test, passed, feedback, ok=True):
        docstring = test._testMethodDoc or ""
        
        task_number_match = re.search(r"[Tt]ask(\d+)", str(test), re.DOTALL)
        task_number = task_number_match.group(1) if task_number_match else "General"

        name_match = re.search(r"#name\((.*?)\)", docstring, re.DOTALL)

        # Test name like this: "Task 1: Test the cool function number 3"
        test_name_prefix = f"{'Task ' + task_number}: "
        test_name = f"{test_name_prefix}{name_match.group(1).strip() if name_match else test._testMethodName}"

        score_match = re.search(r"#score\((\d+)\)", docstring, re.DOTALL)
        score = 0 if not passed else (int(score_match.group(1)) if score_match else 1)
        
        hidden_test = bool(re.search(r"#hidden", docstring, re.DOTALL))
        private_test = bool(re.search(r"#private", docstring, re.DOTALL))
        approach_test = bool(re.search(r"#approach", docstring, re.DOTALL))
        
        hurdle_test = bool(re.search(r"#hurdle", docstring, re.DOTALL))
        self.any_hurdles_failed = self.any_hurdles_failed or (hurdle_test and not passed)

        # Update the Ed output
        result = {
            "name": test_name,
            "score": 0,
            "ok": ok,
            "passed": passed,
            "feedback": feedback.strip(),
            "hidden": hidden_test,
            "private": private_test,
        }
        self.test_results.append(result)
        
        # Make sure the aggregate results are created
        self._ensure_aggregate_results(task_number)
        
        # Update the aggregate results if it's not a hurdle test
        if not hurdle_test:
            if approach_test:
                self.aggregate_results["approach"]["score"] += score
            else:
                self.aggregate_results["tests"]["score"] += score
    
    def apply_hurdle(self):
        """
        Hurdle tests are those that should just give 0 marks if they fail.
        The main example is using Python built-ins for tasks that don't allow it.

        Call this before printing the results to apply the hurdle test logic.
        It will set the score to 0 if any hurdle test failed.
        """
        if self.any_hurdles_failed:
            self.aggregate_results["tests"]["score"] = 0
            self.aggregate_results["approach"]["score"] = 0

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
    test_files = [test_file.replace(".py", "").replace("/", ".").replace("\\", ".") for test_file in get_matching_files(file_pattern)]

    if not test_files:
        print("No matching test files found.")
        sys.exit(1)
    
    
    loader = unittest.TestLoader()
    
    if running_in_ed:
        # If we are running in Ed, set buffer=True to avoid getting student's prints out in the console
        runner = unittest.TextTestRunner(resultclass=SingleTaskTestResult, verbosity=0, buffer=True)
        
        # Run all files, save the result in a list
        all_results = []
        for test_file in test_files:
            suite = loader.loadTestsFromName(test_file)
            result: SingleTaskTestResult = runner.run(suite)
            result.apply_hurdle()
            all_results.extend(result.test_results)

        # Reorder the results and bring the aggregate results to the end
        all_results = sorted(all_results, key=lambda x: 1 if "[Aggregate]" in x["name"] else 0)
        
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
