from unittest import TestCase

from ed_utils.decorators import number, visibility
from lazy_double_table import LazyDoubleTable


class TestTask2(TestCase):

    def setUp(self) -> None:
        self.step_table: LazyDoubleTable = LazyDoubleTable()

    @number("2.1")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_step_hash_valid(self):
        test_keys = ["key1", "key2", "key3"]
        for i, key_name in enumerate(test_keys):
            self.step_table[key_name] = i
            self.assertEqual(self.step_table[key_name], i, "HashyStepTable not setting/getting values correctly")
        self.assertEqual(len(self.step_table), len(test_keys), f"Expected {len(test_keys)} keys in HashyStepTable, got {len(self.step_table)}")

    @number("2.2")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_step_hash_delete(self):
        test_keys = ["key1", "key2", "key3"]
        for i, test_key in enumerate(test_keys):
            self.step_table[test_key] = i

        for i, test_key in enumerate(test_keys):
            del self.step_table[test_key]
            self.assertRaises(KeyError, lambda: self.step_table[test_key])
            self.assertEqual(len(self.step_table), len(test_keys) - i - 1, f"Expected {len(test_keys) - i - 1} keys in HashyStepTable, got {len(self.step_table)}")

    @number("2.3")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_step_hash_delete_advanced(self):
        self.step_table = LazyDoubleTable([97])
        self.step_table.hash = lambda _: 0
        lookup_table = ['A', 'B', 'C', 'D', 'E']

        for letter in lookup_table:
            self.step_table[letter] = letter

        for letter in lookup_table:
            self.assertEqual(self.step_table[letter], letter, "HashyStepTable not setting/getting values correctly")

        for i, letter in enumerate(lookup_table):
            del self.step_table[letter]
            self.assertRaises(KeyError, lambda: self.step_table[letter])
            for j in range(i + 1, len(lookup_table)):
                try:
                    self.assertEqual(
                        self.step_table[lookup_table[j]],
                        lookup_table[j],
                        f"After deleting {letter}, expected {lookup_table[j]} to still have its original value"
                    )
                except KeyError:
                    self.fail(f"Key {lookup_table[j]} not found in HashyStepTable after deleting {letter}")

            self.assertEqual(len(self.step_table), len(lookup_table) - i - 1, "HashyStepTable length not updating correctly after deletion")
