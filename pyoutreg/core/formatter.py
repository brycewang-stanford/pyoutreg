"""
Formatter for regression results with professional styling.
Handles decimal places, significance stars, and table layout.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from .regression_parser import RegressionResult
from .options import OutregOptions


class ResultFormatter:
    """Formats regression results for output."""
    
    def __init__(self, options: OutregOptions):
        self.options = options
        
    def format_regression_table(self, results: List[RegressionResult]) -> pd.DataFrame:
        """Format multiple regression results into a comparison table."""
        
        if not results:
            raise ValueError("No regression results provided")
        
        # Get all unique parameter names
        all_params = set()
        for result in results:
            all_params.update(result.param_names)
        all_params = sorted(list(all_params))
        
        # Apply keep/drop filters
        if self.options.keep is not None:
            all_params = [p for p in all_params if p in self.options.keep]
        elif self.options.drop is not None:
            all_params = [p for p in all_params if p not in self.options.drop]
        
        # Build the table
        table_data = []
        
        # Header row with model names
        header = ['Variable']
        for i, result in enumerate(results):
            model_name = result.model_name or f"Model {i+1}"
            if hasattr(self.options, 'ctitle') and self.options.ctitle:
                if isinstance(self.options.ctitle, list):
                    model_name = self.options.ctitle[i] if i < len(self.options.ctitle) else model_name
                elif i == len(results) - 1:  # Last result gets the ctitle
                    model_name = self.options.ctitle
            header.append(model_name)
        
        table_data.append(header)
        
        # Add coefficients and standard errors
        for param in all_params:
            # Coefficient row
            coeff_row = [param]
            se_row = ['']
            
            for result in results:
                if param in result.param_names:
                    coeff = result.coefficients[param]
                    se = result.std_errors[param]
                    pval = result.pvalues[param]
                    
                    # Apply eform transformation if needed
                    if self.options.eform and result.model_type in ['Logit', 'Probit']:
                        coeff = np.exp(coeff)
                    
                    # Format coefficient with significance stars
                    coeff_str = self._format_number(coeff, self.options.bdec)
                    coeff_str += self._get_significance_stars(pval)
                    coeff_row.append(coeff_str)
                    
                    # Format standard error
                    se_str = f"({self._format_number(se, self.options.sdec)})"
                    se_row.append(se_str)
                else:
                    coeff_row.append('')
                    se_row.append('')
            
            table_data.append(coeff_row)
            table_data.append(se_row)
        
        # Add model statistics
        self._add_model_statistics(table_data, results)
        
        # Convert to DataFrame
        df = pd.DataFrame(table_data[1:], columns=table_data[0])
        
        return df
    
    def _add_model_statistics(self, table_data: List[List[str]], results: List[RegressionResult]):
        """Add model statistics to the table."""
        
        # Add separator
        table_data.append([''] * (len(results) + 1))
        
        # Number of observations
        if self.options.include_nobs:
            nobs_row = ['Observations']
            for result in results:
                nobs_row.append(str(result.nobs))
            table_data.append(nobs_row)
        
        # R-squared
        if self.options.include_rsq:
            rsq_row = ['R-squared']
            for result in results:
                rsq = result.statistics.get('rsquared')
                if rsq is not None:
                    rsq_row.append(self._format_number(rsq, 3))
                else:
                    rsq_row.append('')
            table_data.append(rsq_row)
        
        # F-statistic
        if self.options.include_fstat:
            fstat_row = ['F-statistic']
            for result in results:
                fstat = result.statistics.get('fvalue')
                if fstat is not None:
                    fstat_row.append(self._format_number(fstat, 2))
                else:
                    fstat_row.append('')
            table_data.append(fstat_row)
        
        # Add user-specified statistics
        if self.options.addstat:
            for stat_name, stat_value in self.options.addstat.items():
                stat_row = [stat_name]
                if isinstance(stat_value, (list, tuple)):
                    for val in stat_value:
                        stat_row.append(self._format_number(val, 3))
                else:
                    stat_row.append(self._format_number(stat_value, 3))
                    # Fill remaining columns with empty strings
                    while len(stat_row) < len(results) + 1:
                        stat_row.append('')
                table_data.append(stat_row)
    
    def _format_number(self, value: float, decimal_places: int) -> str:
        """Format a number with specified decimal places."""
        if pd.isna(value) or value is None:
            return ''
        # Handle string values (return as-is)
        if isinstance(value, str):
            return value
        # Handle numeric values
        try:
            return f"{value:.{decimal_places}f}"
        except (ValueError, TypeError):
            # If conversion fails, return string representation
            return str(value)
    
    def _get_significance_stars(self, pvalue: float) -> str:
        """Get significance stars based on p-value."""
        if pd.isna(pvalue):
            return ''
        if pvalue < 0.01:
            return '***'
        elif pvalue < 0.05:
            return '**'
        elif pvalue < 0.1:
            return '*'
        else:
            return ''
    
    def format_summary_stats(self, data: pd.DataFrame, 
                           variables: Optional[List[str]] = None) -> pd.DataFrame:
        """Format summary statistics table."""
        
        if variables is None:
            variables = list(data.select_dtypes(include=[np.number]).columns)
        
        # Apply keep/drop filters
        if self.options.keep is not None:
            variables = [v for v in variables if v in self.options.keep]
        elif self.options.drop is not None:
            variables = [v for v in variables if v not in self.options.drop]
        
        stats_data = []
        
        # Header
        stats_data.append(['Variable', 'N', 'Mean', 'Std Dev', 'Min', 'Max'])
        
        for var in variables:
            if var in data.columns:
                series = data[var].dropna()
                row = [
                    var,
                    str(len(series)),
                    self._format_number(series.mean(), 3),
                    self._format_number(series.std(), 3),
                    self._format_number(series.min(), 3),
                    self._format_number(series.max(), 3)
                ]
                stats_data.append(row)
        
        return pd.DataFrame(stats_data[1:], columns=stats_data[0])
    
    def add_title_and_notes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add title and notes to the formatted table."""
        
        result_df = df.copy()
        
        # Add title if specified
        if self.options.title:
            # Insert title row at the top
            title_row = pd.DataFrame([[self.options.title] + [''] * (len(df.columns) - 1)], 
                                   columns=df.columns)
            result_df = pd.concat([title_row, result_df], ignore_index=True)
        
        # Add notes if specified and not disabled
        if self.options.addnote and not self.options.nonotes:
            # Add notes at the bottom
            note_row = pd.DataFrame([[self.options.addnote] + [''] * (len(df.columns) - 1)], 
                                  columns=df.columns)
            result_df = pd.concat([result_df, note_row], ignore_index=True)
        
        # Add default significance note if not disabled
        if not self.options.nonotes:
            sig_note = "*** p<0.01, ** p<0.05, * p<0.1"
            sig_row = pd.DataFrame([[sig_note] + [''] * (len(df.columns) - 1)], 
                                 columns=df.columns)
            result_df = pd.concat([result_df, sig_row], ignore_index=True)
        
        return result_df
