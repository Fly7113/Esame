import unittest
from esame import ExamException
from esame import CSVTimeseriesFile
from esame import compute_increments

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
        self.assertEqual(CSVTimeseriesFile(name=filename).name, filename)

    def test_file_valid(self):
        ts_file = CSVTimeseriesFile(name='test.csv')
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

class TestComputeIncrements(unittest.TestCase):
    def test_valid_range(self):
        data = [
            ['2010-01', 1],
            ['2011-01', 2],
            ['2012-01', 3],
            ['2013-01', 4],
            ['2014-01', 5],
            ['2015-01', 6],
            ['2016-01', 7],
            ['2017-01', 8],
            ['2018-01', 9]
        ]
        first_year = '2011'
        last_year = '2017'
        expected_result = {
            '2011-2012': 1.0,
            '2012-2013': 1.0,
            '2013-2014': 1.0,
            '2014-2015': 1.0,
            '2015-2016': 1.0,
            '2016-2017': 1.0
        }
        self.assertEqual(compute_increments(data, first_year, last_year), expected_result)

    def test_invalid_range(self):
        data = [
            ['2010-01', 1],
            ['2011-01', 2],
            ['2012-01', 3],
            ['2013-01', 4],
            ['2014-01', 5],
            ['2015-01', 6],
            ['2016-01', 7],
            ['2017-01', 8],
            ['2018-01', 9]
        ]
        first_year = '2019'
        last_year = '2020'
        with self.assertRaises(ExamException):
            compute_increments(data, first_year, last_year)

    def test_non_numeric_year(self):
        data = [
            ['2010-01', 1],
            ['2011-01', 2],
            ['2012-01', 3],
            ['2013-01', 4],
            ['2014-01', 5],
            ['2015-01', 6],
            ['2016-01', 7],
            ['2017-01', 8],
            ['2018-01', 9]
        ]
        first_year = '2011'
        last_year = 'abc'
        with self.assertRaises(ExamException):
            compute_increments(data, first_year, last_year)

    def test_first_year_greater_than_last_year(self):
        data = [
            ['2010-01', 1],
            ['2011-01', 2],
            ['2012-01', 3],
            ['2013-01', 4],
            ['2014-01', 5],
            ['2015-01', 6],
            ['2016-01', 7],
            ['2017-01', 8],
            ['2018-01', 9]
        ]
        first_year = '2018'
        last_year = '2017'
        with self.assertRaises(ExamException):
            compute_increments(data, first_year, last_year)

if __name__ == '__main__':
    unittest.main()