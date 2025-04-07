from unittest import TestCase

import ast
import inspect

from tests.helper import CollectionsFinder

from lazy_double_table import LazyDoubleTable


class TestTask2Setup(TestCase):
    def setUp(self) -> None:
        self.step_table: LazyDoubleTable = LazyDoubleTable()
        self.large_table_table_sizes = [24593, 49157, 98317, 196613, 393241, 786433, 1572869]
        self.large_step_table: LazyDoubleTable = LazyDoubleTable(self.large_table_table_sizes)
        self.non_prime_step_table = LazyDoubleTable([6000, 8000, 10000])
        self.sample_keys = ["key1", "key2", "A", "B", "123", "456", "SlightlyLongerKey"]


class TestTask2(TestTask2Setup):
    def test_hash_functions_available(self):
        """
        #name(Test if the hash functions are available)
        """
        self.assertTrue(hasattr(self.step_table, "hash"), "LazyDoubleTable should have a hash function")
        self.assertTrue(hasattr(self.step_table, "hash2"), "LazyDoubleTable should have a hash2 function")

    def test_step_hash_empty(self):
        """
        #name(Test if the hash table is empty at the start)
        """
        self.assertEqual(len(self.step_table), 0, "LazyDoubleTable should be empty at the start")

    def test_setting_items(self):
        """
        #name(Test if the items are set correctly in the hash table)
        """
        for i, key_name in enumerate(self.sample_keys):
            self.step_table[key_name] = i
            self.assertEqual(self.step_table[key_name], i, "LazyDoubleTable not setting/getting values correctly")

        self.assertEqual(
            len(self.step_table),
            len(self.sample_keys), 
            f"Expected {len(self.sample_keys)} keys in LazyDoubleTable, got {len(self.step_table)}"
        )

    def test_step_hash_delete(self):
        """
        #name(Test deleting from the hash table)
        """
        for i, test_key in enumerate(self.sample_keys):
            self.step_table[test_key] = i

        for i, test_key in enumerate(self.sample_keys):
            del self.step_table[test_key]
            self.assertRaises(KeyError, lambda: self.step_table[test_key])
            self.assertEqual(len(self.step_table), len(self.sample_keys) - i - 1, f"Expected {len(self.sample_keys) - i - 1} keys in LazyDoubleTable, got {len(self.step_table)}")

    def test_get_keys(self):
        """
        #name(Test if the keys are returned correctly)
        """
        for i, key in enumerate(self.sample_keys):
            self.step_table[key] = i
        
        keys = self.step_table.keys()
        for i, key in enumerate(keys):
            self.assertIn(key, keys, f"Key {key} not found in LazyDoubleTable returned keys")
        self.assertEqual(len(keys), len(self.sample_keys), f"Expected {len(self.sample_keys)} keys in LazyDoubleTable, got {len(keys)}")

    def test_get_values(self):
        """
        #name(Test if the values are returned correctly)
        """
        for i, key in enumerate(self.sample_keys):
            self.step_table[key] = i
        
        values = self.step_table.values()
        for i, key in enumerate(values):
            self.assertIn(key, values, f"Value {key} not found in LazyDoubleTable returned values")
        self.assertEqual(len(values), len(self.sample_keys), f"Expected {len(self.sample_keys)} keys in LazyDoubleTable, got {len(values)}")

    def test_rehash(self):
        """
        #name(Test if rehashing works correctly)
        """
        for i, key in enumerate(self.sample_keys):
            self.large_step_table[key] = i
        self.large_step_table._LazyDoubleTable__rehash()
        for i, key in enumerate(self.sample_keys):
            self.assertEqual(self.large_step_table[key], i, "LazyDoubleTable not setting/getting values correctly after rehashing")


class TestTask2Approach(TestTask2Setup):
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        """
        import lazy_double_table
        modules = [lazy_double_table]
        
        for f in modules:
            # Get the source code
            f_source = inspect.getsource(f)
            filename = f.__file__
            
            tree = ast.parse(f_source)
            visitor = CollectionsFinder(filename)
            visitor.visit(tree)
            
            # Report any failures
            for failure in visitor.failures:
                self.fail(failure)

    def test_lazy_deletion_1(self):
        """
        #name(Test if lazy deletion works correctly)
        #approach
        """
        for i, key in enumerate(self.sample_keys):
            self.large_step_table[key] = i
        
        # Make sure there are the right number of empty spots in the table initially
        expected_none_count = self.large_step_table.table_size - len(self.sample_keys)
        observed_none_count = sum([1 if x is None else 0 for x in self.large_step_table._LazyDoubleTable__array])
        self.assertEqual(
            observed_none_count,
            expected_none_count,
            f"Expected {expected_none_count} None values in LazyDoubleTable, got {observed_none_count}"
        )

        # Now delete one by one, make sure the empty spots don't increase (because of lazy deletion)
        for i, key in enumerate(self.sample_keys):
            del self.large_step_table[key]
            self.assertRaises(KeyError, lambda: self.large_step_table[key])
            self.assertEqual(
                len(self.large_step_table),
                len(self.sample_keys) - i - 1,
                f"Expected {len(self.sample_keys) - i - 1} keys in LazyDoubleTable, got {len(self.large_step_table)}"
            )
            
            # The number of None values should NOT increase if they have lazy deletion
            observed_none_count = sum([1 if x is None else 0 for x in self.large_step_table._LazyDoubleTable__array])
            self.assertEqual(
                observed_none_count,
                expected_none_count,
                f"Expected {expected_none_count} None values in LazyDoubleTable, got {observed_none_count}"
            )
