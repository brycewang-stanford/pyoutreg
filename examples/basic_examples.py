"""
Basic usage examples for pyoutreg.

This script demonstrates how to use pyoutreg to export regression results
and statistics to Excel and Word formats.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Try to import required packages
try:
    import statsmodels.api as sm
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False
    print("Warning: statsmodels not available. Some examples will be skipped.")

try:
    import linearmodels.panel as lmp
    HAS_LINEARMODELS = True
except ImportError:
    HAS_LINEARMODELS = False
    print("Warning: linearmodels not available. Panel model examples will be skipped.")

# Import pyoutreg
try:
    from pyoutreg import outreg, summary_stats, cross_tab, outreg_compare
    HAS_PYOUTREG = True
except ImportError:
    HAS_PYOUTREG = False
    print("Error: pyoutreg not available. Make sure to install it first.")


def create_sample_data():
    """Create sample dataset for demonstrations."""
    np.random.seed(42)
    n = 1000
    
    data = pd.DataFrame({
        'y': np.random.normal(10, 5, n),
        'x1': np.random.normal(0, 1, n),
        'x2': np.random.normal(2, 1.5, n),
        'x3': np.random.normal(-1, 0.8, n),
        'group': np.random.choice(['A', 'B', 'C'], n),
        'binary': np.random.choice([0, 1], n),
        'id': np.repeat(range(100), 10),  # Panel ID
        'time': np.tile(range(10), 100)   # Time periods
    })
    
    # Create dependent variable with some relationship
    data['y'] = 5 + 2*data['x1'] + -1.5*data['x2'] + 0.8*data['x3'] + np.random.normal(0, 2, n)
    
    return data


def example_basic_regression():
    """Basic OLS regression example."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic OLS Regression")
    print("="*60)
    
    if not (HAS_STATSMODELS and HAS_PYOUTREG):
        print("Skipping: Missing required packages")
        return
    
    # Create sample data
    data = create_sample_data()
    
    # Prepare variables
    y = data['y']
    X = sm.add_constant(data[['x1', 'x2', 'x3']])
    
    # Fit model
    model = sm.OLS(y, X)
    result = model.fit()
    
    print("Model fitted successfully")
    print(f"R-squared: {result.rsquared:.3f}")
    print(f"N: {result.nobs}")
    
    # Export to Excel
    try:
        outreg(result, 'basic_regression.xlsx', replace=True, 
               title="Basic OLS Regression Results",
               addnote="This is a demonstration of pyoutreg basic functionality")
        print("✓ Results exported to basic_regression.xlsx")
    except Exception as e:
        print(f"✗ Excel export failed: {e}")
    
    # Export to Word
    try:
        outreg(result, 'basic_regression.docx', replace=True,
               title="Basic OLS Regression Results")
        print("✓ Results exported to basic_regression.docx")
    except Exception as e:
        print(f"✗ Word export failed: {e}")


def example_model_comparison():
    """Multiple model comparison example."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Multiple Model Comparison")
    print("="*60)
    
    if not (HAS_STATSMODELS and HAS_PYOUTREG):
        print("Skipping: Missing required packages")
        return
    
    # Create sample data
    data = create_sample_data()
    
    # Model 1: Simple regression
    y = data['y']
    X1 = sm.add_constant(data[['x1']])
    result1 = sm.OLS(y, X1).fit()
    
    # Model 2: Multiple regression
    X2 = sm.add_constant(data[['x1', 'x2']])
    result2 = sm.OLS(y, X2).fit()
    
    # Model 3: Full model
    X3 = sm.add_constant(data[['x1', 'x2', 'x3']])
    result3 = sm.OLS(y, X3).fit()
    
    print("Three models fitted for comparison")
    
    # Export comparison table
    try:
        outreg_compare(
            [result1, result2, result3],
            'model_comparison.xlsx',
            model_names=['Simple', 'Multiple', 'Full'],
            title="Model Comparison: Progressive Addition of Variables",
            replace=True
        )
        print("✓ Comparison table exported to model_comparison.xlsx")
    except Exception as e:
        print(f"✗ Comparison export failed: {e}")


def example_logit_regression():
    """Logistic regression example."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Logistic Regression")
    print("="*60)
    
    if not (HAS_STATSMODELS and HAS_PYOUTREG):
        print("Skipping: Missing required packages")
        return
    
    # Create sample data
    data = create_sample_data()
    
    # Prepare binary dependent variable
    y_binary = data['binary']
    X = sm.add_constant(data[['x1', 'x2', 'x3']])
    
    # Fit logit model
    logit_model = sm.Logit(y_binary, X)
    logit_result = logit_model.fit()
    
    print("Logit model fitted successfully")
    print(f"Pseudo R-squared: {logit_result.prsquared:.3f}")
    
    # Export coefficients
    try:
        outreg(logit_result, 'logit_coefficients.xlsx', replace=True,
               ctitle="Coefficients", 
               title="Logistic Regression Results")
        print("✓ Coefficients exported to logit_coefficients.xlsx")
    except Exception as e:
        print(f"✗ Coefficients export failed: {e}")
    
    # Export odds ratios
    try:
        outreg(logit_result, 'logit_odds_ratios.xlsx', replace=True,
               ctitle="Odds Ratios", eform=True,
               title="Logistic Regression Results (Odds Ratios)")
        print("✓ Odds ratios exported to logit_odds_ratios.xlsx")
    except Exception as e:
        print(f"✗ Odds ratios export failed: {e}")


def example_summary_statistics():
    """Summary statistics example."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Summary Statistics")
    print("="*60)
    
    if not HAS_PYOUTREG:
        print("Skipping: Missing pyoutreg")
        return
    
    # Create sample data
    data = create_sample_data()
    
    print("Data created with variables:", list(data.columns))
    
    # Basic summary statistics
    try:
        summary_stats(data, 'summary_stats.xlsx', 
                     variables=['y', 'x1', 'x2', 'x3'],
                     replace=True,
                     title="Summary Statistics")
        print("✓ Summary statistics exported to summary_stats.xlsx")
    except Exception as e:
        print(f"✗ Summary statistics export failed: {e}")
    
    # Detailed summary statistics
    try:
        summary_stats(data, 'detailed_stats.xlsx',
                     variables=['y', 'x1', 'x2', 'x3'],
                     detail=True, replace=True,
                     title="Detailed Summary Statistics")
        print("✓ Detailed statistics exported to detailed_stats.xlsx")
    except Exception as e:
        print(f"✗ Detailed statistics export failed: {e}")
    
    # Grouped summary statistics
    try:
        summary_stats(data, 'grouped_stats.xlsx',
                     variables=['y', 'x1', 'x2'],
                     by='group', replace=True,
                     title="Summary Statistics by Group")
        print("✓ Grouped statistics exported to grouped_stats.xlsx")
    except Exception as e:
        print(f"✗ Grouped statistics export failed: {e}")


def example_cross_tabulation():
    """Cross-tabulation example."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Cross-tabulation")
    print("="*60)
    
    if not HAS_PYOUTREG:
        print("Skipping: Missing pyoutreg")
        return
    
    # Create sample data
    data = create_sample_data()
    
    print("Creating cross-tabulation table")
    
    # Cross-tabulation
    try:
        cross_tab(data, 'group', 'binary', 'crosstab.xlsx',
                 replace=True,
                 title="Cross-tabulation: Group vs Binary Variable")
        print("✓ Cross-tabulation exported to crosstab.xlsx")
    except Exception as e:
        print(f"✗ Cross-tabulation export failed: {e}")


def example_customization():
    """Advanced customization example."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Advanced Customization")
    print("="*60)
    
    if not (HAS_STATSMODELS and HAS_PYOUTREG):
        print("Skipping: Missing required packages")
        return
    
    # Create sample data
    data = create_sample_data()
    
    # Fit model
    y = data['y']
    X = sm.add_constant(data[['x1', 'x2', 'x3']])
    result = sm.OLS(y, X).fit()
    
    print("Demonstrating advanced customization options")
    
    # Highly customized output
    try:
        outreg(result, 'customized_output.xlsx', replace=True,
               title="Highly Customized Regression Output",
               ctitle="Custom Model",
               bdec=4,  # 4 decimal places for coefficients
               sdec=3,  # 3 decimal places for standard errors
               keep=['x1', 'x2'],  # Only show x1 and x2
               addnote="Note: x3 coefficient excluded for brevity",
               addstat={'Custom Stat': 42.0, 'Another Stat': 3.14},
               font_size=12,
               nonotes=False)
        print("✓ Customized output exported to customized_output.xlsx")
    except Exception as e:
        print(f"✗ Customized export failed: {e}")


def main():
    """Run all examples."""
    print("PyOutreg Examples")
    print("================")
    print("This script demonstrates the key features of pyoutreg")
    
    # Check if required packages are available
    if not HAS_PYOUTREG:
        print("\nError: pyoutreg not available.")
        print("Please install pyoutreg first:")
        print("pip install -e .")
        return
    
    # Run examples
    example_basic_regression()
    example_model_comparison()
    example_logit_regression()
    example_summary_statistics()
    example_cross_tabulation()
    example_customization()
    
    print("\n" + "="*60)
    print("EXAMPLES COMPLETED")
    print("="*60)
    print("\nCheck the current directory for output files:")
    print("- basic_regression.xlsx/docx")
    print("- model_comparison.xlsx")
    print("- logit_coefficients.xlsx")
    print("- logit_odds_ratios.xlsx")
    print("- summary_stats.xlsx")
    print("- detailed_stats.xlsx")
    print("- grouped_stats.xlsx")
    print("- crosstab.xlsx")
    print("- customized_output.xlsx")


if __name__ == "__main__":
    main()
