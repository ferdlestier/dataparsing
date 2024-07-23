import unittest
import logging
import pandas as pd
from parser import main

class TestParser(unittest.TestCase):

    def setUp(self):
        # Set up any necessary preconditions for the tests
        self.log_file = 'parser.log'
        self.csv_file = 'minhaReq2.20220126.csv'
        self.df = pd.read_csv(self.csv_file)

    def tearDown(self):
        # Clean up after tests
        pass

    def test_script_execution(self):
        # Test the execution of the parser script
        try:
            main()
        except Exception as e:
            self.fail(f"Script execution failed with exception: {e}")

    def test_logging_functionality(self):
        # Test the logging functionality
        with open(self.log_file, 'r') as log:
            logs = log.read()
            self.assertIn("Script started", logs)
            self.assertIn("Script completed successfully", logs)

    def test_error_handling(self):
        # Test the error handling functionality
        try:
            main()
        except Exception as e:
            with open(self.log_file, 'r') as log:
                logs = log.read()
                self.assertIn("Error occurred", logs)

    def test_data_parsing(self):
        # Test the data parsing functionality
        self.assertIsInstance(self.df, pd.DataFrame)
        self.assertFalse(self.df.empty)

    def test_data_analysis(self):
        # Test the data analysis functionality
        dailymovers = self.df.sort_values(by='chgPct1D', ascending=False).head(20)
        self.assertEqual(len(dailymovers), 20)
        self.assertIn('ticker', dailymovers.columns)

if __name__ == '__main__':
    unittest.main()
