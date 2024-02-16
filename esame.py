# ===================== #
# Cutom exception class #
# ===================== #
class ExamException(Exception):
    """
    Exception class for exam-related errors.
    """
    pass

# ============= #
# CSVFile class #
# ============= #
class CSVFile:
    """
    Represents a CSV file.

    Attributes:
        name (str): The name of the file.
        readable (bool): Indicates if the file is readable.
    """

    def __init__(self, name):
        """
        Initializes an instance of the Exam class.

        Parameters:
        name (str): The name of the file to be opened.

        Raises:
        ExamException: If there is an error opening the file.
        """
        # Set the file name
        self.name = name
        
        # Set the readability flag to False
        self.readable = False
        # Test if the file is readable
        try:
            # Open the file
            my_file = open(self.name, 'r')
            # Read the first line
            my_file.readline()
            # Set the flag to True
            self.readable = True
        except Exception as e:
            # If the file is not readable, raise an exception
            raise ExamException("Errore in apertura del file: {}".format(e))

# ======================= #
# CSVTimeseriesFile class #
# ======================= #
class CSVTimeseriesFile(CSVFile):
    """
    Represents a CSV file containing timeseries data.

    Attributes:
        name (str): The name of the file.
    """

    def __init__(self, name):
        """
        Initializes a new instance of the CSVTimeseriesFile class.

        Args:
            name (str): The name of the file.
        """
        # Set the file name
        self.name = name

    def get_data(self):
        """
        Reads the CSV file and returns the timeseries data.

        Returns:
            list: A list of nested lists representing the timeseries data.
                  Each nested list contains a date (in the format YYYY-MM) and a numeric value.
        """
        
        # Initialize the list
        data = []

        # Test if the file is openable
        try:
            file = open(self.name, 'r')
        except Exception as e:
            # If the file is not openable, raise an exception
            raise ExamException("Errore in apertura del file: {}".format(e))

        # Read each line of the file
        for line in file:
            # The key value pair is split at the comma
            elements = line.split(',')

            # Remove leading and trailing whitespaces
            elements[0] = elements[0].strip()

            # Any string shorter or longer than 7 characters is not a date in the format YYYY-MM
            if len(elements[0]) != 7:
                continue

            # Any string that doesn't have a '-' in the 5th position is not a date in the format YYYY-MM
            if elements[0][4] != '-':
                continue

            try:
                # Extract the year and the month
                year = int(elements[0][0:4])
                month = int(elements[0][5:7])
            except ValueError:
                # Catch only ValueError exceptions: any string whose first 4 or last 2 characters are not numeric is not a date in the format YYYY-MM
                continue
            
            # Any string whose last 2 characters are not between 1 and 12 is not a date in the format YYYY-MM
            if month < 1 or month > 12:
                continue

            # Any year out of range is not acceptable
            if year < 1949 or year > 1960:
                continue

            if len(data) > 0:
                # Check if the year is older than the last year in the list or if the year is the same and the month is older than or the same of the last month in the list
                if year < int(data[-1][0][0:4]) or (year == int(data[-1][0][0:4]) and month <= int(data[-1][0][5:7])):
                    if year == int(data[-1][0][0:4]) and month == int(data[-1][0][5:7]):
                        # If the date is duplicated, raise an exception
                        raise ExamException("Errore: date duplicate")
                    else:
                        # If the date older than the last date in the list, raise an exception
                        raise ExamException("Errore: date non in ordine")

            # Check if the value of the second element is numeric and integer
            try:
                elements[1] = int(elements[1])
            except ValueError:
                # If the values are not numeric and integer, skip the line
                continue


            # Add the key value pair to the list
            data.append(elements[0:2])
        
        # Close the file
        file.close()

        # Return the list of nested lists
        return data

def compute_increments(data, first_year, last_year):
    """
    Compute the positive increments of yearly averages within a given range of years.

    Parameters:
    - data (list): A list of lists containing yearly data.
    - first_year (str): The first year of interest.
    - last_year (str): The last year of interest.

    Returns:
    - increments (dict | list): A dictionary containing the years as keys and the positive increments as values.
                         If no positive increments are found, an empty list is returned.
    """

    # Initialize the list averages (format: [[year, average], ...])
    averages = []

    # Initialize the list deltas between averages (format: [[year(n)-year(n+1), delta], ...])
    deltas = []

    # Initialize the dictionary of positive increments (format: {year(n)-year(n+1): increment, ...})
    increments = {}

    # Check if the first_year and last_year are strings
    if not isinstance(first_year, str):
        raise ExamException("Errore: il primo anno non è passato come stringa")
    if not isinstance(last_year, str):
        raise ExamException("Errore: il secondo anno non è passato come stringa")

    # If the first_year is not an integer, raise an exception
    try:
        first_year = int(first_year)
    except ValueError:
        raise ExamException("Errore: primo anno non numerico")
    # If the last_year is not an integer, raise an exception
    try:
        last_year = int(last_year)
    except ValueError:
        raise ExamException("Errore: secondo anno non numerico")

    # Check if the first_year is less than or equal to the last_year
    if first_year >= last_year:
        # If the first_year is greater than the last_year, raise an exception
        raise ExamException("Errore: primo anno maggiore o uguale all'ultimo")

    # Check if the first_year and last_year are in the range of the data provided
    if first_year < int(data[0][0][0:4]) or last_year > int(data[-1][0][0:4]):
        # If the first_year and last_year are not in the range of the data provided, raise an exception
        raise ExamException("Errore: anno non in range")
    

    # Initialize the variables to calculate the averages
    year = data[0][0][0:4]
    sum = 0
    count = 0

    # Iterate over the list of nested lists
    for i in range(len(data)):
        # Check if the year has changed
        if data[i][0][0:4] != year:
            # Add the year and the average to the list
            averages.append([year, sum / count])
            # Update the variables
            year = data[i][0][0:4]
            sum = 0
            count = 0
        # Update the variables
        sum += data[i][1]
        count += 1

    # Add the last year and the average to the list
    averages.append([year, sum / count])

    # Iterate over the list of averages
    for i in range(len(averages) - 1):
        # Calculate the delta
        delta = averages[i + 1][1] - averages[i][1]
        # Add the delta to the list
        deltas.append([averages[i][0] + '-' + averages[i + 1][0], delta])

    # Iterate over the list of deltas
    for i in range(len(deltas)):
        # Check if the year is in the range of interest
        if int(deltas[i][0][0:4]) >= first_year and int(deltas[i][0][5:9]) <= last_year:
            # Check if the delta is positive
            if deltas[i][1] > 0:
                # Add the year and the positive increment to the dictionary
                increments[deltas[i][0]] = deltas[i][1]

    # Return the dictionary if it is not empty, otherwise return an empty list
    if len(increments) > 0:
        return increments
    else:
        return []