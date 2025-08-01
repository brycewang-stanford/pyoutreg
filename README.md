# PyOutreg

[![PyPI version](https://badge.fury.io/py/pyoutreg.svg)](https://badge.fury.io/py/pyoutreg)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyoutreg.svg)](https://pypi.org/project/pyoutreg/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/brycewang-stanford/pyoutreg.svg?style=social&label=Star)](https://github.com/brycewang-stanford/pyoutreg)
[![PyPI downloads](https://img.shields.io/pypi/dm/pyoutreg.svg)](https://pypi.org/project/pyoutreg/)

A Python implementation of Stata's popular `outreg2` command for exporting regression results to Excel and Word formats with publication-quality formatting.

## 🎯 Features

- **📊 Regression Export**: Export results from `statsmodels` and `linearmodels` to Excel (.xlsx) and Word (.docx)
- **🔬 Model Support**: OLS, Fixed Effects, Random Effects, Logit, Probit, IV, Panel Data
- **📋 Professional Formatting**: Publication-ready tables with significance stars, standard errors
- **📈 Model Comparison**: Side-by-side comparison of multiple models in single tables
- **🎨 Customization**: Extensive options for decimal places, variable selection, titles, notes
- **📊 Summary Statistics**: Descriptive statistics and cross-tabulation export
- **🔗 Integration**: Part of the **pystatar** ecosystem for Stata-like functionality in Python

## 🚀 Installation

```bash
pip install pyoutreg
```

## 🌐 Related Packages

PyOutreg is part of a growing ecosystem of Python packages that bring Stata-like functionality to Python:

### [PyStataR](https://github.com/brycewang-stanford/PyStataR)
The **PyOutreg** library will be integrated into **PyStataR**, a comprehensive Python package that bridges Stata and R functionality in Python. PyStataR aims to provide Stata users with familiar commands and workflows while leveraging Python's powerful data science ecosystem.

### [StasPAI](https://github.com/brycewang-stanford/StasPAI)
For users interested in AI-powered econometric analysis, **StasPAI** offers a related project focused on integrating statistical analysis with artificial intelligence methods. StasPAI provides advanced econometric modeling capabilities enhanced by machine learning approaches.

**Package Ecosystem:**
- **[PyStataR](https://github.com/brycewang-stanford/PyStataR)** - Main package that integrates PyOutreg and other Stata-like tools
- **[StasPAI](https://github.com/brycewang-stanford/StasPAI)** - AI-powered econometric analysis and machine learning integration
- **PyOutreg** - Regression table export functionality (this package)

PyOutreg will be integrated into the **PyStataR** package to provide a comprehensive Stata-like experience in Python.

## 📖 Quick Start

### Basic Regression Export

```python
import pandas as pd
import statsmodels.api as sm
from pyoutreg import outreg

# Load data and run regression
data = pd.read_csv('your_data.csv')
y = data['wage']
X = sm.add_constant(data[['education', 'experience', 'age']])
result = sm.OLS(y, X).fit()

# Export to Excel with professional formatting
outreg(result, 'regression_results.xlsx', 
       title="Wage Regression Analysis",
       ctitle="OLS Model",
       replace=True)

# Export to Word with custom notes
outreg(result, 'regression_results.docx',
       title="Wage Regression Analysis", 
       addnote="Standard errors in parentheses. *** p<0.01, ** p<0.05, * p<0.1",
       replace=True)
```

### Multiple Model Comparison

```python
from pyoutreg import outreg_compare

# Fit multiple models
X1 = sm.add_constant(data[['education']])
model1 = sm.OLS(y, X1).fit()

X2 = sm.add_constant(data[['education', 'experience']])
model2 = sm.OLS(y, X2).fit()

X3 = sm.add_constant(data[['education', 'experience', 'age']])
model3 = sm.OLS(y, X3).fit()

# Compare models side-by-side
outreg_compare(
    [model1, model2, model3],
    'model_comparison.xlsx',
    model_names=['Basic', 'Add Experience', 'Full Model'],
    title='Progressive Model Specification',
    replace=True
)
```

### Panel Data Analysis

```python
import linearmodels.panel as lmp

# Prepare panel data
panel_data = data.set_index(['individual_id', 'year'])

# Fixed Effects Model
dependent = panel_data['wage']
exogenous = panel_data[['education', 'experience']]

fe_model = lmp.PanelOLS(dependent, exogenous, entity_effects=True)
fe_result = fe_model.fit(cov_type='clustered', cluster_entity=True)

# Random Effects Model  
re_model = lmp.RandomEffects(dependent, exogenous)
re_result = re_model.fit()

# Compare panel models
outreg_compare(
    [fe_result, re_result],
    'panel_comparison.xlsx',
    model_names=['Fixed Effects', 'Random Effects'],
    title='Panel Data Model Comparison',
    replace=True
)
```

### Logistic Regression with Odds Ratios

```python
# Binary outcome regression
y_binary = data['employed']  # 1=employed, 0=unemployed
X_logit = sm.add_constant(data[['education', 'experience', 'age']])

logit_model = sm.Logit(y_binary, X_logit)
logit_result = logit_model.fit()

# Export coefficients
outreg(logit_result, 'logit_coefficients.xlsx',
       title="Employment Probability Analysis",
       ctitle="Coefficients",
       replace=True)

# Export odds ratios
outreg(logit_result, 'logit_odds_ratios.xlsx',
       title="Employment Probability Analysis",
       ctitle="Odds Ratios",
       eform=True,  # Convert to odds ratios
       replace=True)
```

### Summary Statistics

```python
from pyoutreg import summary_stats

# Basic descriptive statistics
summary_stats(
    data,
    'summary_stats.xlsx',
    variables=['wage', 'education', 'experience', 'age'],
    title="Descriptive Statistics",
    replace=True
)

# Grouped statistics
summary_stats(
    data,
    'grouped_stats.xlsx', 
    variables=['wage', 'education'],
    by='gender',  # Group by gender
    title="Statistics by Gender",
    replace=True
)

# Detailed statistics with percentiles
summary_stats(
    data,
    'detailed_stats.xlsx',
    variables=['wage', 'education'],
    detail=True,  # Include percentiles, skewness, kurtosis
    title="Detailed Descriptive Statistics",
    replace=True
)
```

### Cross-tabulation

```python
from pyoutreg import cross_tab

# Cross-tabulation with counts and percentages
cross_tab(
    data,
    'gender',      # Row variable
    'region',      # Column variable  
    'crosstab_gender_region.xlsx',
    title="Gender by Region Cross-tabulation",
    replace=True
)
```

### Advanced Customization

```python
# Extensive customization options
outreg(result, 'customized_output.xlsx',
       replace=True,
       title="Wage Regression with Custom Formatting",
       ctitle="Full Model",
       
       # Decimal control
       dec=3,          # Overall decimal places
       bdec=4,         # Coefficient decimal places
       sdec=5,         # Standard error decimal places
       
       # Variable selection
       keep=['education', 'experience'],  # Only show these variables
       # drop=['age'],  # Alternative: drop specific variables
       
       # Additional statistics
       addstat={
           'Mean Wage': data['wage'].mean(),
           'Sample Size': len(data),
           'Data Period': '2010-2020'
       },
       
       # Notes and formatting
       addnote="Robust standard errors. Data from national survey.",
       font_size=12
)

```

## 🎛️ API Reference

### Main Functions

#### `outreg(model_result, filename, **options)`
Export single regression model to Excel or Word.

**Parameters:**
- `model_result`: Fitted regression model (statsmodels or linearmodels)
- `filename`: Output filename (.xlsx or .docx) or None for preview
- `ctitle`: Column title for the model
- `title`: Table title
- `replace`: Replace existing file (default: False)
- `append`: Append to existing file (default: False)
- `dec/bdec/sdec`: Decimal places for overall/coefficients/standard errors
- `keep/drop`: Variable selection
- `addstat`: Dictionary of additional statistics
- `addnote`: Custom notes
- `eform`: Export odds ratios for logistic regression

#### `outreg_compare(models_list, filename, **options)`
Compare multiple models side-by-side.

**Parameters:**
- `models_list`: List of fitted regression models
- `filename`: Output filename or None for preview
- `model_names`: List of model names
- `title`: Table title
- Other options same as `outreg`

#### `summary_stats(data, filename, **options)`
Export descriptive statistics.

**Parameters:**
- `data`: pandas DataFrame
- `filename`: Output filename or None for preview
- `variables`: List of variables to include
- `by`: Grouping variable
- `detail`: Include percentiles and distribution statistics

#### `cross_tab(data, row_var, col_var, filename, **options)`
Export cross-tabulation table.

**Parameters:**
- `data`: pandas DataFrame
- `row_var`: Row variable name
- `col_var`: Column variable name
- `filename`: Output filename or None for preview

## 🎨 Output Examples

### Regression Table Output
```
                     Variable    Model 1    Model 2    Model 3
                    education   482.135***  462.891***  458.023***
                                (24.726)    (25.018)   (25.134)
                   experience               301.274***  287.345***
                                             (18.642)   (19.123)
                          age                           156.789***
                                                       (12.456)
                     Constant  15234.567*** 12845.321*** 11234.789***
                                (387.234)   (425.178)   (456.234)
                                 
                 Observations       1,000       1,000       1,000
                    R-squared       0.234       0.287       0.312
                  F-statistic      152.34      189.45      167.23
*** p<0.01, ** p<0.05, * p<0.1
```

### Summary Statistics Output
```
Variable       Obs      Mean    Std. Dev.      Min       Max
wage         1,000  45,234.56   12,456.78  15,000   120,000
education    1,000      15.8         2.4        8        25
experience   1,000      12.3         8.9        0        40
age          1,000      35.2        10.1       18        65
```

## 🔗 Integration with PyStataR

PyOutreg is designed to be integrated into the **PyStataR** package, which aims to provide comprehensive Stata-like functionality in Python:

```python
# Future integration (planned)
import PyStataR as ps

# Will include PyOutreg functionality
ps.outreg(model, 'results.xlsx')
ps.summary_stats(data, 'stats.xlsx')

# Along with other Stata-like commands
ps.regress('wage education experience age', data)
ps.summarize(data)
ps.tabulate('gender region', data)
```

**Related Projects:**
- **PyStataR**: Main integration package providing Stata-like functionality
- **StasPAI**: AI-powered econometric analysis with machine learning integration
- **PyOutreg**: Regression table export (this package)

## 📚 Documentation

For comprehensive documentation and more examples:

- **Tutorial**: See `tutorial.ipynb` for a complete walkthrough
- **Examples**: Check the `examples/` directory for specific use cases
- **API Reference**: Detailed function documentation
- **Tests**: `tests/` directory contains validation examples

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

MIT License
