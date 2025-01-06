import unittest
import logging
import pandas as pd
from parser import main
from fpdf import FPDF
import os

class TestParser(unittest.TestCase):

    def setUp(self):
        # Set up any necessary preconditions for the tests
        self.log_file = 'parser.log'
        self.csv_file = 'minhaReq2.20220126.csv'
        self.df = pd.read_csv(self.csv_file)
        self.pdf_file = 'report.pdf'

    def tearDown(self):
        # Clean up after tests
        if os.path.exists(self.pdf_file):
            os.remove(self.pdf_file)

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

    def test_pdf_generation(self):
        # Test the PDF report generation
        main()
        self.assertTrue(os.path.exists(self.pdf_file))

        # Check if the PDF contains expected data
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.output(self.pdf_file)

        with open(self.pdf_file, 'rb') as pdf_file:
            content = pdf_file.read()
            self.assertIn(b'Top 20 Daily Movers', content)
            self.assertIn(b'Top 20 Daily Losers', content)
            self.assertIn(b'Top 20 Medium Term Price Change (Growth)', content)
            self.assertIn(b'Top 20 Medium Term Price Change (Loss)', content)
            self.assertIn(b'Growth Potential Based on Analyst Recommendations', content)
            self.assertIn(b'Top 20 Financial Exposure', content)
            self.assertIn(b'Top 20 Return on Invested Capital', content)
            self.assertIn(b'Top 20 Fundamental Data', content)

if __name__ == '__main__':
    unittest.main()
