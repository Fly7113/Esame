import unittest

from esame import *
import test_esame


def main():
    ts_file = CSVTimeseriesFile(name='data.csv')
    ts = ts_file.get_data()
    print("\nTime series data:")
    print(ts)
    print("\nYearly averages:")
    print(calc_yearly_averages(ts))
    print("\nYearly deltas:")
    print(calc_yearly_averages_deltas(ts))
    print("\nPositive yearly deltas from range 1949-1960:")
    print(compute_increments(ts, "1949", "1960"))
    print("\nUnit tests:")
    tests = unittest.TestLoader().loadTestsFromModule(test_esame)
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    main()