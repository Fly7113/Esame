import unittest

from esame import *
import test_esame


def main():
    ts_file = CSVTimeseriesFile(name='data.csv')
    ts = ts_file.get_data()
    min_max = find_min_max(ts)
    print("\nTime series data:")
    print(ts)
    print("\nMinimum and maximum values:")
    print(min_max)
    print("\nUnit tests:")
    tests = unittest.TestLoader().loadTestsFromModule(test_esame)
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    main()