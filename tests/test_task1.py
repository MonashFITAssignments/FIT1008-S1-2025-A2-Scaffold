from unittest import TestCase
import ast
import inspect

from tests.helper import CollectionsFinder

from hashy_date_table import HashyDateTable

from datetime import datetime, timedelta
from random_gen import RandomGen


class TestTask1Setup(TestCase):
    def setUp(self) -> None:
        self.uniform_table: HashyDateTable = HashyDateTable()
        self.test_dates_simple_1 = ['2005-01-06', '2025-03-02', '1998-01-23']
        self.test_dates_simple_2 = ['2012/10/01', '1978/11/22', '2020/06/19']
        self.test_dates_simple_3 = ['15-05-2024', '16-02-2025', '07-03-1989']
        self.test_dates_simple_4 = ['28/02/2025', '02/09/2000', '14/12/2007']


class TestTask1(TestTask1Setup):
    def _run_simple_operations_on_one_date_format(self, test_dates: list[str]):
        """
        The purpose of this function is to test different date formats separately, allowing partial marks.
        """
        for i, test_date in enumerate(test_dates):
            self.uniform_table[test_date] = "String Value " + str(i)
            self.assertEqual(self.uniform_table[test_date], "String Value " + str(i), "HashyDateTable not setting/getting values correctly")
        self.assertEqual(len(self.uniform_table), len(test_dates), f"Expected {len(test_dates)} in HashyDateTable, got {len(self.uniform_table)}")

    def test_uniform_hash_simple_1(self):
        """        
        #name(Test the date table with YYYY-MM-DD format)
        """
        self._run_simple_operations_on_one_date_format(self.test_dates_simple_1)
    
    def test_uniform_hash_simple_2(self):
        """
        #name(Test the date table with YYYY/MM/DD format)
        """
        self._run_simple_operations_on_one_date_format(self.test_dates_simple_2)
    
    def test_uniform_hash_simple_3(self):
        """
        #name(Test the date table with DD-MM-YYYY format)
        """
        self._run_simple_operations_on_one_date_format(self.test_dates_simple_3)
    
    def test_uniform_hash_simple_4(self):
        """
        #name(Test the date table with DD/MM/YYYY format)
        """
        self._run_simple_operations_on_one_date_format(self.test_dates_simple_4)

    def test_uniform_hash_delete_public(self):
        """
        #name(Test simple deleting from the date table)
        """
        test_dates = self.test_dates_simple_1
        for i, test_date in enumerate(test_dates):
            self.uniform_table[test_date] = "String Value " + str(i)

        for i, test_date in enumerate(test_dates):
            del self.uniform_table[test_date]
            self.assertRaises(KeyError, lambda: self.uniform_table[test_date])
            self.assertEqual(
                len(self.uniform_table),
                len(test_dates) - i - 1, 
                f"Expected {len(test_dates) - i - 1} keys in HashyDateTable after deletion, got {len(self.uniform_table)}"
            )


class TestTask1Approach(TestTask1Setup):
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        """
        import hashy_date_table
        modules = [hashy_date_table]

        for f in modules:
            # Get the source code
            f_source = inspect.getsource(f)
            filename = f.__file__
            
            tree = ast.parse(f_source)
            visitor = CollectionsFinder(filename)
            visitor.visit(tree)
            
            # Report any failures
            for failure in visitor.failures:
                klass, func, used_type, message = failure
                if klass == "HashyDateTable" and func == "__init__" and used_type == list:
                    # Ignore the use of Python list in the constructor
                    continue
                self.fail(message)

    def test_table_size(self):
        """
        #name(Table size is not changed to avoid conflicts)
        #approach
        """
        self.assertEqual(self.uniform_table.table_size, 366, "Table size is not 366 upon creation")
        for key in [
            (datetime(2000, 1, 1) + timedelta(days=i)).strftime('%Y-%m-%d')
            for i in range(365)
        ]:
            self.uniform_table[key] = "String Value"
        self.assertEqual(self.uniform_table.table_size, 4*366, "Table size is not 4*366 after inserting 365 items")
    
    def _common_logic_of_single_year_hashing_test(self):
        first_day = datetime.strptime("2025-01-01", '%Y-%m-%d')

        all_year_days = [
            (first_day + timedelta(days=i)).strftime('%Y-%m-%d')
            for i in range(365)
        ]

        # Randomise the order
        RandomGen.random_shuffle(all_year_days)

        hash_values = [self.uniform_table.hash(date) for date in all_year_days]
        hash_values_set = set(hash_values)
        return len(all_year_days) - len(hash_values_set)

    def test_uniformity_single_year_basic(self):
        """        
        #name(Test the uniformity of the date table in 1 year with leniency)
        #approach
        """
        duplicates = self._common_logic_of_single_year_hashing_test()
        # Check that the number of duplicates is at most 0.03 of the number of days
        self.assertLessEqual(duplicates, 0.03 * 365, "Hash function is not uniform enough")

    def _common_logic_of_multi_year_hashing_test(self):
        """
        This method helps testing the same logic with different 'slacks'
        """

        # Immediately rehash to get a larger table
        self.uniform_table._LinearProbeTable__rehash()
        # Check that the table size is 4 * 366
        self.assertEqual(self.uniform_table.table_size, 4 * 366, "HashyDateTable not rehashing correctly")
        # Check that the number of elements is 0
        self.assertEqual(len(self.uniform_table), 0, "HashyDateTable not rehashing correctly")
        # Check that the table is empty
        self.assertTrue(self.uniform_table.is_empty(), "HashyDateTable not rehashing correctly")

        # Now we can test the uniformity of the hash function
        # Generate a list of all days in 4 years
        all_days = []
        for year in range(4):
            # Doing this in 2 loops to avoid leap years eating up a day from the next year
            first_day = datetime.strptime(f"{str(2025 + year)}-01-01", '%Y-%m-%d')
            all_days += [
                (first_day + timedelta(days = i)).strftime('%Y-%m-%d')
                for i in range(365)
            ]

        # Randomise the order
        RandomGen.random_shuffle(all_days)

        hash_values = [self.uniform_table.hash(date) for date in all_days]
        prob_simulation_table = [0] * (4 * 366)
        for hash_value in hash_values:
            prob_simulation_table[hash_value] += 1
        
        # Iterate through the table, make sure there are enough empty spaces in between
        # so the number of collisions is never too high
        current_collisions = 0
        max_observed_collisions = 0
        for i in range(len(prob_simulation_table)):
            current_collisions += prob_simulation_table[i]
            if current_collisions > 0:
                current_collisions -= 1
            max_observed_collisions = max(max_observed_collisions, current_collisions)
        return max_observed_collisions

    def test_uniformity_multiple_years_basic(self):
        """
        #name(Test the uniformity of the date table in 4 years with high leniency)
        #approach
        """
        max_observed_collisions = self._common_logic_of_multi_year_hashing_test()
        # Check that the maximum number of collisions is at most 3% of the number of days
        self.assertLessEqual(max_observed_collisions, 0.03 * 4 * 365, "Hash function is not uniform enough")
