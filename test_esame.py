import unittest
from esame import ExamException
from esame import CSVTimeseriesFile

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

if __name__ == '__main__':
    unittest.main()