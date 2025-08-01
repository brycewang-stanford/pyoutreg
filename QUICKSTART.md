# PyOutreg Installation and Quick Start Guide

## Installation

### Option 1: Install from source (Recommended for development)

1. **Clone or download the pyoutreg package**
   ```bash
   cd /Users/brycewang/pyoutreg
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install in development mode**
   ```bash
   pip install -e .
   ```

### Option 2: Install required packages individually

If you want to install just the dependencies:

```bash
pip install pandas numpy statsmodels linearmodels openpyxl python-docx scipy
```

## Quick Start

### 1. Basic Regression Export

```python
import pandas as pd
import statsmodels.api as sm
from pyoutreg import outreg

# Load your data
data = pd.read_csv('your_data.csv')

# Prepare variables
y = data['dependent_variable']
X = sm.add_constant(data[['var1', 'var2', 'var3']])

# Fit regression
result = sm.OLS(y, X).fit()

# Export to Excel
outreg(result, 'regression_results.xlsx', replace=True)

# Export to Word
outreg(result, 'regression_results.docx', replace=True)
```

### 2. Multiple Model Comparison

```python
# Fit multiple models
result1 = sm.OLS(y, X1).fit()
result2 = sm.OLS(y, X2).fit()
result3 = sm.OLS(y, X3).fit()

# Export comparison table
from pyoutreg import outreg_compare

outreg_compare(
    [result1, result2, result3],
    'model_comparison.xlsx',
    model_names=['Simple', 'Multiple', 'Full'],
    title='Model Comparison'
)
```

### 3. Summary Statistics

```python
from pyoutreg import summary_stats

# Basic summary statistics
summary_stats(data, 'summary.xlsx', 
             variables=['var1', 'var2', 'var3'],
             replace=True)

# Detailed summary statistics with percentiles
summary_stats(data, 'detailed_summary.xlsx',
             variables=['var1', 'var2', 'var3'],
             detail=True, replace=True)

# Grouped summary statistics
summary_stats(data, 'grouped_summary.xlsx',
             variables=['var1', 'var2'],
             by='group_variable', replace=True)
```

### 4. Cross-tabulation

```python
from pyoutreg import cross_tab

cross_tab(data, 'category1', 'category2', 
         'crosstab.xlsx', replace=True)
```

## Advanced Usage

### Customization Options

```python
outreg(result, 'custom_output.xlsx',
       replace=True,
       title="Custom Regression Table",
       ctitle="My Model",
       dec=3,                    # Overall decimal places
       bdec=4,                   # Coefficient decimal places
       sdec=2,                   # Standard error decimal places
       keep=['var1', 'var2'],    # Only show specific variables
       addnote="Custom note here",
       addstat={'F-stat': result.fvalue, 'Custom': 42.0},
       font_size=12,
       landscape=True)           # Word documents only
```

### Panel Data Models

```python
import linearmodels.panel as lmp

# Fixed effects regression
mod = lmp.PanelOLS(y, X, entity_effects=True)
result = mod.fit()

outreg(result, 'panel_results.xlsx', 
       ctitle="Fixed Effects", replace=True)
```

### Logistic Regression

```python
# Logit model
logit_result = sm.Logit(y_binary, X).fit()

# Export coefficients
outreg(logit_result, 'logit_coef.xlsx', 
       ctitle="Coefficients", replace=True)

# Export odds ratios
outreg(logit_result, 'logit_or.xlsx',
       ctitle="Odds Ratios", eform=True, replace=True)
```

## Supported Model Types

- **statsmodels**: OLS, Logit, Probit, GLM
- **linearmodels**: PanelOLS (Fixed/Random Effects), IV regression
- Any model with similar result interface (params, bse, tvalues, pvalues)

## Output Formats

- **Excel (.xlsx)**: Professional tables with formatting, borders, fonts
- **Word (.docx)**: Publication-ready tables with proper styling

## Key Features

- ✅ Multiple model comparison in single tables
- ✅ Professional publication-quality formatting
- ✅ Extensive customization options
- ✅ Summary statistics and cross-tabulations
- ✅ Support for various regression types
- ✅ Automatic significance stars
- ✅ Custom notes and statistics
- ✅ Variable selection (keep/drop)
- ✅ Decimal place control

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure all dependencies are installed
   ```bash
   pip install pandas numpy statsmodels linearmodels openpyxl python-docx scipy
   ```

2. **File Permission Error**: Close Excel/Word files before running export

3. **Module Not Found**: Install pyoutreg in development mode
   ```bash
   pip install -e .
   ```

### Getting Help

1. Check the examples in `examples/basic_examples.py`
2. Run the test suite: `python tests/test_pyoutreg.py`
3. Review the docstrings in the code

## Comparison with Stata's outreg2

PyOutreg implements most key features of Stata's outreg2:

| Feature | Stata outreg2 | PyOutreg | Notes |
|---------|---------------|----------|-------|
| Basic regression export | ✅ | ✅ | |
| Multiple model comparison | ✅ | ✅ | |
| Excel/Word export | ✅ | ✅ | |
| Decimal control (dec, bdec, sdec) | ✅ | ✅ | |
| Variable selection (keep, drop) | ✅ | ✅ | |
| Custom titles and notes | ✅ | ✅ | |
| Summary statistics | ✅ | ✅ | |
| Cross-tabulation | ✅ | ✅ | |
| Label support | ✅ | ⚠️ | Partial support |
| Fixed effects notation | ✅ | ✅ | |
| Odds ratios (eform) | ✅ | ✅ | |

## Next Steps

1. **Try the examples**: Run `python examples/basic_examples.py`
2. **Test with your data**: Start with simple exports and gradually add customization
3. **Explore advanced features**: Panel models, grouped statistics, etc.
4. **Integrate into workflow**: Use in Jupyter notebooks or Python scripts

Enjoy using PyOutreg! 🎉
