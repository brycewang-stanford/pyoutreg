# PyOutReg (outreg2)

[![PyPI version](https://badge.fury.io/py/pyoutreg.svg)](https://badge.fury.io/py/pyoutreg)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyoutreg.svg)](https://pypi.org/project/pyoutreg/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/brycewang-stanford/pyoutreg.svg?style=social&label=Star)](https://github.com/brycewang-stanford/pyoutreg)
[![PyPI downloads](https://img.shields.io/pypi/dm/pyoutreg.svg)](https://pypi.org/project/pyoutreg/)

A Python implementation of Stata's popular `outreg2` command for exporting regression results to Excel and Word formats with publication-quality formatting.

##  Features

- **Regression Export**: Export results from `statsmodels` and `linearmodels` to Excel (.xlsx) and Word (.docx)
- **Model Support**: OLS, Fixed Effects, Random Effects, Logit, Probit, IV, Panel Data
- **Professional Formatting**: Publication-ready tables with significance stars, standard errors
- **Model Comparison**: Side-by-side comparison of multiple models in single tables
- **Customization**: Extensive options for decimal places, variable selection, titles, notes
- **Summary Statistics**: Descriptive statistics and cross-tabulation export
- **Ecosystem Integration**: Part of the **statar** ecosystem for comprehensive Stata and R-like functionality in Python
- **Future-Ready**: Designed for seamless integration with **pdtab**, **pywinsor2**, **pyegen**, and other statistical tools

##  Installation

```bash
pip install pyoutreg
```

##  Related Packages

PyOutreg is part of a growing ecosystem of Python packages that bring Stata-like functionality to Python:

### [statar](https://github.com/brycewang-stanford/statar)
The **PyOutreg** library will be integrated into **statar**, a comprehensive Python package that provides Stata and R-like functionality in Python. statar aims to provide Stata users with familiar commands and workflows while leveraging Python's powerful data science ecosystem.

### [StasPAI](https://github.com/brycewang-stanford/StasPAI)
For users interested in AI-powered analysis, **StasPAI** offers a related project focused on integrating statistics, econometrics, machine learning, and LLMs/AI methods. StasPAI provides advanced analytical capabilities that combine traditional statistical methods with modern AI approaches.

##  Integration with Broader Ecosystem

**PyOutreg** is part of a comprehensive statistical analysis ecosystem:

### [statar](https://github.com/brycewang-stanford/statar)
The **PyOutreg** library will be integrated into **statar**, a comprehensive Python package that provides Stata-like functionality in Python. statar aims to provide Stata users with familiar commands and workflows while leveraging Python's powerful data science ecosystem.

**Key Integration Features:**
- **Unified Command Interface**: PyOutreg's `outreg()` function will be accessible as `st.outreg()` within statar
- **Seamless Workflow**: Direct integration with statar's regression commands and data manipulation functions
- **Consistent Syntax**: Stata-like command structure for familiar user experience
- **Enhanced Functionality**: Combined with other statistical tools for comprehensive analysis

### [StasPAI](https://github.com/brycewang-stanford/StasPAI)
**StasPAI** is a related but independent project that focuses on integrating statistics, econometrics, machine learning, and LLMs/AI methods. It provides advanced analytical capabilities combining traditional statistical methods with modern AI approaches.

**Ecosystem Components:**
- **[statar](https://github.com/brycewang-stanford/statar)** - Main package integrating PyOutreg and other Stata-like tools
- **[pdtab](https://github.com/brycewang-stanford/pdtab)** - Pandas-based tabulation library for cross-tabulation and summary statistics
- **[pywinsor2](https://github.com/brycewang-stanford/pywinsor2)** - Winsorization and outlier treatment utilities
- **[pyegen](https://github.com/brycewang-stanford/pyegen)** - Data generation and variable creation tools
- **PyOutreg** - Regression table export functionality (this package)
- **[StasPAI](https://github.com/brycewang-stanford/StasPAI)** - AI-powered statistical analysis (related package)

### Future Integration Examples
```python
# Future statar integration
import statar as st

# Regression analysis with immediate export
st.regress('wage education experience age', data)
st.outreg('regression_results.xlsx', title="Wage Analysis")

# Combined workflow with integrated tools
st.summarize(data)
st.tabulate('gender region', data)  # pdtab integration
st.winsor2('wage', data, p=[0.01, 0.99])  # pywinsor2 integration
st.egen('wage_group = cut(wage)', data)   # pyegen integration
st.outreg_compare([model1, model2], 'comparison.xlsx')
```

##  Quick Start

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

## API Reference

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

## Output Examples

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
![alt text](image-1.png)

### Summary Statistics Output
```
Variable       Obs      Mean    Std. Dev.      Min       Max
wage         1,000  45,234.56   12,456.78  15,000   120,000
education    1,000      15.8         2.4        8        25
experience   1,000      12.3         8.9        0        40
age          1,000      35.2        10.1       18        65
```

## Integration with statar

PyOutreg is designed to be integrated into the **statar** package, which aims to provide comprehensive Stata-like functionality in Python. As part of the broader statistical ecosystem, PyOutreg will work seamlessly with other Stata-like tools:

```python
# Future integration (planned)
import statar as st

# Direct regression analysis and export
st.regress('wage education experience age', data)
st.outreg('wage_analysis.xlsx', title="Wage Regression Results")

# Summary statistics and cross-tabulation
st.summarize(data, by='gender')
st.tabulate('education region', data)

# Advanced model comparison workflow
model1 = st.regress('wage education', data)
model2 = st.regress('wage education experience', data) 
model3 = st.regress('wage education experience age', data)

st.outreg_compare([model1, model2, model3], 
                 'progressive_models.xlsx',
                 model_names=['Basic', 'Add Experience', 'Full Model'])

# Integration with other ecosystem tools
st.pdtab.crosstab(data, 'gender', 'region')  # pdtab integration
st.winsor2('wage', data, p=[0.01, 0.99])     # pywinsor2 integration
st.egen('wage_decile = xtile(wage)', data)   # pyegen integration
st.summary_stats(data, detail=True)          # PyOutreg functionality
```

**Integrated Ecosystem Benefits:**
- **Unified Interface**: Single import for all Stata-like functionality
- **Seamless Workflow**: No need to switch between different packages
- **Consistent Documentation**: Integrated help system and examples
- **Enhanced Performance**: Optimized integration between components

**Related Projects in the Ecosystem:**
- **[statar](https://github.com/brycewang-stanford/statar)**: Main integration package providing Stata-like functionality
- **[pdtab](https://github.com/brycewang-stanford/pdtab)**: Pandas-based tabulation library for statistical summaries
- **[pywinsor2](https://github.com/brycewang-stanford/pywinsor2)**: Winsorization and outlier treatment utilities
- **[pyegen](https://github.com/brycewang-stanford/pyegen)**: Data generation and variable creation tools
- **PyOutreg**: Regression table export (this package)

**Related but Independent:**
- **[StasPAI](https://github.com/brycewang-stanford/StasPAI)**: AI-powered statistical analysis combining traditional methods with machine learning and LLMs

## Documentation

For comprehensive documentation and more examples:

- **Tutorial**: See `tutorial.ipynb` for a complete walkthrough
- **Examples**: Check the `examples/` directory for specific use cases
- **API Reference**: Detailed function documentation
- **Tests**: `tests/` directory contains validation examples

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

MIT License

Copyright (c) 2025 Bryce Wang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
