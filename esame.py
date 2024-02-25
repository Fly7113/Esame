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