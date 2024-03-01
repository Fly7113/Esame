import unittest
from esame import ExamException
from esame import CSVTimeSeriesFile
from esame import find_min_max

class TestExamException(unittest.TestCase):
    def test_message(self):
        with self.assertRaises(ExamException) as cm:
            raise ExamException("This is the message")
        self.assertEqual(str(cm.exception), "This is the message")

    def test_default_message(self):
        with self.assertRaises(ExamException) as cm:
            raise ExamException()
        self.assertEqual(str(cm.exception), "")

    def test_default_message_with_args(self):
        with self.assertRaises(ExamException) as cm:
            raise ExamException("This is the message", "This is the second message")
        self.assertEqual(str(cm.exception), "('This is the message', 'This is the second message')")

class TestCSVTimeseriesFile(unittest.TestCase):
    def test_file_not_found(self):
        filename = 'file_not_found.csv'
        self.assertEqual(CSVTimeSeriesFile(name=filename).name, filename)

    def test_file_valid(self):
        ts_file = CSVTimeSeriesFile(name='test.csv')
        self.assertEqual(ts_file.get_data(), [
            ['1949-01', 1],
            ['1950-01', 2],
            ['1951-01', 3],
            ['1952-01', 4],
            ['1953-01', 5],
            ['1954-01', 6],
            ['1955-01', 7],
            ['1956-01', 8],
            ['1957-01', 9]
        ])

class TestFindMinMax(unittest.TestCase):
    def test_single_month_year(self):
        data = [['2022-01', 10]]
        expected_result = {'2022': {'min': ['01'], 'max': ['01']}}
        self.assertEqual(find_min_max(data), expected_result)

    def test_multiple_months_year(self):
        data = [['2022-01', 10], ['2022-02', 20], ['2022-03', 15]]
        expected_result = {'2022': {'min': ['01'], 'max': ['02']}}
        self.assertEqual(find_min_max(data), expected_result)

    def test_multiple_months_year_same_value(self):
        data = [['2022-01', 10], ['2022-02', 10], ['2022-03', 10]]
        expected_result = {'2022': {'min': ['01', '02', '03'], 'max': ['01', '02', '03']}}
        self.assertEqual(find_min_max(data), expected_result)

    def test_multiple_years(self):
        data = [['2022-01', 10], ['2022-02', 20], ['2023-01', 5], ['2023-02', 15]]
        expected_result = {'2022': {'min': ['01'], 'max': ['02']}, '2023': {'min': ['01'], 'max': ['02']}}
        self.assertEqual(find_min_max(data), expected_result)

if __name__ == '__main__':
    unittest.main()