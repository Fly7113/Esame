# Esame
This repository contains the solution to the exam of the lab of the course "Indroduzione alla Programmazione" of the Bachelor's Degree in Artificial Intelligence and Data Analytics (AIDA) at the University of Trieste.

## `esame.py`
The file `esame.py` contains an ExamException class, a `CSVFile` class, a `CSVTimeSeriesFile` class extending the `CSVFile` class and defining a method `get_data`, a function `compute_increments` and 2 other helper functions, namely `calc_yearly_averages` and `calc_yearly_averages_deltas`.

## `test_esame.py`
The file `test_esame.py` contains the tests for the `esame.py` file, using unittest.

## `data.csv` and `test.csv`
The file `data.csv` contains the data used for the manual tests.
The file `test.csv` contains the data used for the automatic tests done by unittest.

## `main.py`
The file `main.py` contains the main function that reads the data from the file `data.csv` and prints the yearly averages and the yearly averages deltas, and executes the unittests.