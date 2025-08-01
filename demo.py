"""
Simple demonstration of pyoutreg functionality.
This script creates sample data and demonstrates basic usage without external dependencies.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

# Set random seed for reproducible results
np.random.seed(42)

print("PyOutreg Demonstration")
print("=====================")
print("Creating sample data and demonstrating basic functionality...\n")

# Create sample dataset
n = 1000
data = pd.DataFrame({
    'income': np.random.normal(50000, 15000, n),
    'education': np.random.normal(12, 3, n),
    'experience': np.random.normal(10, 8, n),
    'age': np.random.normal(35, 10, n),
    'gender': np.random.choice(['Male', 'Female'], n),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n)
})

# Create some realistic relationships
data['income'] = (
    30000 + 
    2000 * data['education'] + 
    800 * data['experience'] + 
    200 * data['age'] + 
    np.random.normal(0, 5000, n)
)

# Ensure positive income
data['income'] = np.maximum(data['income'], 15000)

print("Sample data created:")
print(f"- {n} observations")
print(f"- Variables: {list(data.columns)}")
print(f"- Mean income: ${data['income'].mean():.0f}")
print()

# Test basic functionality without external model libraries
print("Testing pyoutreg import...")
try:
    from pyoutreg import outreg, summary_stats, cross_tab
    print("✓ pyoutreg imported successfully")
except ImportError as e:
    print(f"✗ pyoutreg import failed: {e}")
    print("\nTo install pyoutreg dependencies:")
    print("pip install pandas numpy openpyxl python-docx")
    print("\nTo install pyoutreg:")
    print("pip install -e .")
    exit(1)

# Test summary statistics
print("\nTesting summary statistics...")
try:
    # Create summary statistics table
    stats_df = summary_stats(
        data, 
        variables=['income', 'education', 'experience', 'age'],
        filename=None  # Return DataFrame instead of saving
    )
    print("✓ Summary statistics computed successfully")
    print("\nSummary Statistics Preview:")
    print(stats_df.to_string(index=False))
    
    # Save to file
    summary_stats(
        data,
        'demo_summary_stats.xlsx',
        variables=['income', 'education', 'experience', 'age'],
        title="Sample Data Summary Statistics",
        replace=True
    )
    print(f"✓ Summary statistics saved to demo_summary_stats.xlsx")
    
except Exception as e:
    print(f"✗ Summary statistics failed: {e}")

# Test cross-tabulation
print("\nTesting cross-tabulation...")
try:
    # Create cross-tabulation table
    crosstab_df = cross_tab(
        data, 
        'gender', 
        'region',
        filename=None  # Return DataFrame instead of saving
    )
    print("✓ Cross-tabulation computed successfully")
    print("\nCross-tabulation Preview:")
    print(crosstab_df.to_string(index=False))
    
    # Save to file
    cross_tab(
        data,
        'gender',
        'region', 
        'demo_crosstab.xlsx',
        title="Gender by Region Cross-tabulation",
        replace=True
    )
    print(f"✓ Cross-tabulation saved to demo_crosstab.xlsx")
    
except Exception as e:
    print(f"✗ Cross-tabulation failed: {e}")

# Test with simulated regression results
print("\nTesting simulated regression export...")
try:
    # Create a mock regression result for demonstration
    class MockRegressionResult:
        def __init__(self):
            self.params = pd.Series([25000, 2500, 800, 150], 
                                  index=['const', 'education', 'experience', 'age'])
            self.bse = pd.Series([2000, 200, 100, 50], 
                               index=['const', 'education', 'experience', 'age'])
            self.tvalues = pd.Series([12.5, 12.5, 8.0, 3.0], 
                                   index=['const', 'education', 'experience', 'age'])
            self.pvalues = pd.Series([0.000, 0.000, 0.000, 0.003], 
                                   index=['const', 'education', 'experience', 'age'])
            self.nobs = 1000
            self.rsquared = 0.65
            self.fvalue = 245.2
            self.f_pvalue = 0.000
            self.rsquared_adj = 0.649
    
    # Create mock result
    mock_result = MockRegressionResult()
    
    # Test that the regression parser can handle it
    from pyoutreg.core.regression_parser import RegressionResult
    
    reg_result = RegressionResult(
        model_type='OLS',
        coefficients=mock_result.params,
        std_errors=mock_result.bse,
        tvalues=mock_result.tvalues,
        pvalues=mock_result.pvalues,
        statistics={
            'rsquared': mock_result.rsquared,
            'fvalue': mock_result.fvalue,
            'f_pvalue': mock_result.f_pvalue
        },
        nobs=mock_result.nobs
    )
    
    print("✓ Mock regression result created successfully")
    
    # Format the results
    from pyoutreg.core.formatter import ResultFormatter
    from pyoutreg.core.options import OutregOptions
    
    options = OutregOptions(
        title="Income Regression Results",
        dec=3,
        addnote="Mock regression for demonstration purposes"
    )
    
    formatter = ResultFormatter(options)
    result_df = formatter.format_regression_table([reg_result])
    result_df = formatter.add_title_and_notes(result_df)
    
    print("✓ Regression table formatted successfully")
    print("\nRegression Table Preview:")
    print(result_df.to_string(index=False))
    
    # Export to Excel
    from pyoutreg.exporters.xlsx_exporter import export_to_excel
    export_to_excel(result_df, 'demo_regression.xlsx', options)
    print(f"✓ Regression results saved to demo_regression.xlsx")
    
except Exception as e:
    print(f"✗ Regression export failed: {e}")

# Check output files
print("\nOutput files created:")
output_files = [
    'demo_summary_stats.xlsx',
    'demo_crosstab.xlsx', 
    'demo_regression.xlsx'
]

for filename in output_files:
    if Path(filename).exists():
        size = Path(filename).stat().st_size
        print(f"✓ {filename} ({size} bytes)")
    else:
        print(f"✗ {filename} (not found)")

print("\nDemonstration completed!")
print("\nNext steps:")
print("1. Install statsmodels: pip install statsmodels")
print("2. Install linearmodels: pip install linearmodels") 
print("3. Run full examples: python examples/basic_examples.py")
print("4. Try with your own data!")

print(f"\nFor more information, see QUICKSTART.md")
