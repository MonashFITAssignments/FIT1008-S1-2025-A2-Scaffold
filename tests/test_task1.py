from unittest import TestCase

from ed_utils.decorators import number, visibility
from hashy_date_table import HashyDateTable
from hashy_step_table import HashyStepTable


class TestTask1(TestCase):

    def setUp(self) -> None:
        self.uniform_table: HashyDateTable = HashyDateTable()
        self.test_dates_simple_1 = ['2005-01-06', '2025-03-02', '1998-01-23']
        self.test_dates_simple_2 = ['2012/10/01', '1978/11/22', '2020/06/19']
        self.test_dates_simple_3 = ['15-05-2024', '16-02-2025', '07-03-1989']
        self.test_dates_simple_4 = ['28/02/2025', '02/09/2000', '14/12/2007']
        self.test_dates_mixed = self.test_dates_simple_1 + self.test_dates_simple_2 + self.test_dates_simple_3 + self.test_dates_simple_4

    # The different date formats are tested separately so the students would get marks for each of the formats they pass
    def _run_simple_operations_on_one_date_format(self, test_dates: list[str]):
        for i, test_date in enumerate(test_dates):
            self.uniform_table[test_date] = "String Value " + str(i)
            self.assertEqual(self.uniform_table[test_date], "String Value " + str(i), "HashyDateTable not setting/getting values correctly")
        self.assertEqual(len(self.uniform_table), len(test_dates), f"Expected {len(test_dates)} in HashyDateTable, got {len(self.uniform_table)}")

    @number("1.1")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_uniform_hash_simple_1(self):
        self._run_simple_operations_on_one_date_format(self.test_dates_simple_1)
    
    @number("1.2")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_uniform_hash_simple_2(self):
        self._run_simple_operations_on_one_date_format(self.test_dates_simple_2)
    
    @number("1.3")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_uniform_hash_simple_3(self):
        self._run_simple_operations_on_one_date_format(self.test_dates_simple_3)
    
    @number("1.4")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_uniform_hash_simple_4(self):
        self._run_simple_operations_on_one_date_format(self.test_dates_simple_4)
    
    @number("1.5")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_uniform_hash_mixed_dates(self):
        for i, test_date in enumerate(self.test_dates_mixed):
            self.uniform_table[test_date] = "String Value " + str(i)
            self.assertEqual(self.uniform_table[test_date], "String Value " + str(i), "HashyDateTable not setting/getting values correctly")
        self.assertEqual(
            len(self.uniform_table),
            len(self.test_dates_mixed),
            f"Expected {len(self.test_dates_mixed)} in HashyDateTable, got {len(self.uniform_table)}"
        )

    @number("1.6")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_uniform_hash_delete(self):
        test_dates = self.test_dates_mixed
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
