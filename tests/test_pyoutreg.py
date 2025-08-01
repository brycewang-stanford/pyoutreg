"""
Test suite for pyoutreg package.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os

# Test imports
try:
    from pyoutreg.core.options import OutregOptions, parse_options
    from pyoutreg.core.formatter import ResultFormatter
    from pyoutreg.utils.statistics import compute_summary_statistics
    PYOUTREG_AVAILABLE = True
except ImportError:
    PYOUTREG_AVAILABLE = False


class TestOutregOptions:
    """Test OutregOptions class."""
    
    def test_default_options(self):
        """Test default option values."""
        if not PYOUTREG_AVAILABLE:
            pytest.skip("pyoutreg not available")
        
        options = OutregOptions()
        assert options.bdec == 3
        assert options.sdec == 3
        assert options.replace == False
        assert options.append == False
        assert options.font_size == 11
    
    def test_decimal_override(self):
        """Test decimal place override."""
        if not PYOUTREG_AVAILABLE:
            pytest.skip("pyoutreg not available")
        
        options = OutregOptions(dec=2)
        assert options.bdec == 2
        assert options.sdec == 2
        
        options = OutregOptions(dec=2, bdec=4)
        assert options.bdec == 4
        assert options.sdec == 2
    
    def test_mutual_exclusivity(self):
        """Test mutually exclusive options."""
        if not PYOUTREG_AVAILABLE:
            pytest.skip("pyoutreg not available")
        
        with pytest.raises(ValueError):
            OutregOptions(replace=True, append=True)
        
        with pytest.raises(ValueError):
            OutregOptions(keep=['x1'], drop=['x2'])


class TestSummaryStatistics:
    """Test summary statistics functionality."""
    
    def create_test_data(self):
        """Create test dataset."""
        np.random.seed(42)
        return pd.DataFrame({
            'x1': np.random.normal(0, 1, 100),
            'x2': np.random.normal(5, 2, 100),
            'x3': np.random.choice(['A', 'B'], 100),
            'x4': np.random.uniform(0, 10, 100)
        })
    
    def test_basic_summary_stats(self):
        """Test basic summary statistics."""
        if not PYOUTREG_AVAILABLE:
            pytest.skip("pyoutreg not available")
        
        data = self.create_test_data()
        result = compute_summary_statistics(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'Variable' in result.columns
        assert 'N' in result.columns
        assert 'Mean' in result.columns
        assert len(result) == 3  # Only numeric columns
    
    def test_variable_selection(self):
        """Test variable selection in summary stats."""
        if not PYOUTREG_AVAILABLE:
            pytest.skip("pyoutreg not available")
        
        data = self.create_test_data()
        options = OutregOptions(keep=['x1', 'x2'])
        result = compute_summary_statistics(data, options=options)
        
        assert len(result) == 2
        assert all(var in ['x1', 'x2'] for var in result['Variable'])


class TestFileOperations:
    """Test file operations and exports."""
    
    def test_file_validation(self):
        """Test filename validation."""
        if not PYOUTREG_AVAILABLE:
            pytest.skip("pyoutreg not available")
        
        from pyoutreg.utils.helpers import validate_filename
        
        # Valid files
        xlsx_path = validate_filename('test.xlsx')
        assert xlsx_path.suffix == '.xlsx'
        
        docx_path = validate_filename('test.docx')
        assert docx_path.suffix == '.docx'
        
        # Invalid file
        with pytest.raises(ValueError):
            validate_filename('test.txt')


class TestFormatter:
    """Test result formatting."""
    
    def test_number_formatting(self):
        """Test number formatting functionality."""
        if not PYOUTREG_AVAILABLE:
            pytest.skip("pyoutreg not available")
        
        options = OutregOptions(bdec=2, sdec=3)
        formatter = ResultFormatter(options)
        
        # Test number formatting
        assert formatter._format_number(3.14159, 2) == "3.14"
        assert formatter._format_number(3.14159, 4) == "3.1416"
    
    def test_significance_stars(self):
        """Test significance star assignment."""
        if not PYOUTREG_AVAILABLE:
            pytest.skip("pyoutreg not available")
        
        options = OutregOptions()
        formatter = ResultFormatter(options)
        
        assert formatter._get_significance_stars(0.001) == "***"
        assert formatter._get_significance_stars(0.02) == "**"
        assert formatter._get_significance_stars(0.08) == "*"
        assert formatter._get_significance_stars(0.15) == ""


class TestEndToEnd:
    """End-to-end integration tests."""
    
    def create_mock_result(self):
        """Create a mock regression result for testing."""
        
        class MockResult:
            def __init__(self):
                self.params = pd.Series([1.5, -0.8, 2.1], index=['const', 'x1', 'x2'])
                self.bse = pd.Series([0.2, 0.15, 0.3], index=['const', 'x1', 'x2'])
                self.tvalues = pd.Series([7.5, -5.3, 7.0], index=['const', 'x1', 'x2'])
                self.pvalues = pd.Series([0.0, 0.001, 0.0], index=['const', 'x1', 'x2'])
                self.nobs = 100
                self.rsquared = 0.75
                self.fvalue = 45.2
                self.f_pvalue = 0.0
                
        return MockResult()
    
    def test_mock_regression_workflow(self):
        """Test complete workflow with mock data."""
        if not PYOUTREG_AVAILABLE:
            pytest.skip("pyoutreg not available")
        
        from pyoutreg.core.regression_parser import RegressionResult
        from pyoutreg.core.formatter import ResultFormatter
        
        # Create mock result
        mock = self.create_mock_result()
        
        # Create RegressionResult
        reg_result = RegressionResult(
            model_type='OLS',
            coefficients=mock.params,
            std_errors=mock.bse,
            tvalues=mock.tvalues,
            pvalues=mock.pvalues,
            statistics={'rsquared': mock.rsquared, 'fvalue': mock.fvalue},
            nobs=mock.nobs
        )
        
        # Format results
        options = OutregOptions()
        formatter = ResultFormatter(options)
        result_df = formatter.format_regression_table([reg_result])
        
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df.columns) == 2  # Variable + Model columns
        assert 'Variable' in result_df.columns


def run_tests():
    """Run all tests manually (for when pytest is not available)."""
    
    print("Running PyOutreg Tests")
    print("======================")
    
    if not PYOUTREG_AVAILABLE:
        print("❌ PyOutreg not available - skipping tests")
        return
    
    test_classes = [
        TestOutregOptions(),
        TestSummaryStatistics(),
        TestFileOperations(),
        TestFormatter(),
        TestEndToEnd()
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        class_name = test_class.__class__.__name__
        print(f"\n{class_name}")
        print("-" * len(class_name))
        
        # Get all test methods
        test_methods = [method for method in dir(test_class) 
                       if method.startswith('test_')]
        
        for method_name in test_methods:
            total_tests += 1
            try:
                method = getattr(test_class, method_name)
                method()
                print(f"✓ {method_name}")
                passed_tests += 1
            except Exception as e:
                print(f"❌ {method_name}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Tests completed: {passed_tests}/{total_tests} passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total_tests - passed_tests} tests failed")


if __name__ == "__main__":
    run_tests()
