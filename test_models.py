import unittest
import pandas as pd
from io import BytesIO
from models import SalesAnalyzer

class TestSalesAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.analyzer = SalesAnalyzer()

    def test_initial_state(self):
        """Test that analyzer starts with None df and peak."""
        self.assertIsNone(self.analyzer.df)
        self.assertIsNone(self.analyzer.peak)
        self.assertFalse(self.analyzer.is_valid)

    def test_load_valid_excel(self):
        """Test loading a valid Excel file with 2 columns."""
        # Create sample data
        dates = pd.date_range('2023-01-01', periods=5)
        sales = [100, 200, 300, 400, 500]
        df = pd.DataFrame({'Date': dates, 'Sales_USD': sales})

        # Convert to Excel bytes
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        # Load the data
        result = self.analyzer.load_sales_excel(buffer.getvalue(), 'test.xlsx')
        self.assertTrue(result)
        self.assertTrue(self.analyzer.is_valid)
        self.assertIsNotNone(self.analyzer.peak)

        # Check peak calculation
        self.assertEqual(self.analyzer.peak.peak_sales, 500.0)
        self.assertEqual(self.analyzer.peak.total_sales, 1500.0)
        self.assertEqual(self.analyzer.peak.avg_sales, 300.0)
        self.assertEqual(self.analyzer.peak.days, 5)

    def test_load_excel_wrong_columns_count(self):
        """Test loading Excel with wrong number of columns."""
        # Create data with 3 columns
        dates = pd.date_range('2023-01-01', periods=3)
        sales = [100, 200, 300]
        extra = [1, 2, 3]
        df = pd.DataFrame({'Date': dates, 'Sales_USD': sales, 'Extra': extra})

        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        result = self.analyzer.load_sales_excel(buffer.getvalue(), 'test.xlsx')
        self.assertFalse(result)
        self.assertFalse(self.analyzer.is_valid)

    def test_load_excel_invalid_data(self):
        """Test loading Excel with invalid data types."""
        # Create data with non-numeric sales
        dates = pd.date_range('2023-01-01', periods=3)
        sales = ['a', 'b', 'c']  # Invalid sales data
        df = pd.DataFrame({'Date': dates, 'Sales_USD': sales})

        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        result = self.analyzer.load_sales_excel(buffer.getvalue(), 'test.xlsx')
        self.assertFalse(result)
        self.assertFalse(self.analyzer.is_valid)

    def test_load_excel_insufficient_data(self):
        """Test loading Excel with less than 2 rows."""
        # Create data with only 1 row
        dates = pd.date_range('2023-01-01', periods=1)
        sales = [100]
        df = pd.DataFrame({'Date': dates, 'Sales_USD': sales})

        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        result = self.analyzer.load_sales_excel(buffer.getvalue(), 'test.xlsx')
        self.assertFalse(result)
        self.assertFalse(self.analyzer.is_valid)

    def test_create_peak_sales_graph(self):
        """Test that graph creation works when data is loaded."""
        # First load valid data
        dates = pd.date_range('2023-01-01', periods=5)
        sales = [100, 200, 300, 400, 500]
        df = pd.DataFrame({'Date': dates, 'Sales_USD': sales})

        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        self.analyzer.load_sales_excel(buffer.getvalue(), 'test.xlsx')

        # Now test graph creation
        graph_json = self.analyzer.create_peak_sales_graph()
        self.assertIsInstance(graph_json, str)
        self.assertGreater(len(graph_json), 0)

if __name__ == '__main__':
    unittest.main()