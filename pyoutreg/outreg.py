"""
Main interface for pyoutreg - Python implementation of Stata's outreg2.

This module provides the main outreg() function and related utilities for
exporting regression results and statistics to Excel and Word formats.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, List, Optional, Dict, Any
import warnings

# Import core modules
from .core.options import parse_options, OutregOptions
from .core.regression_parser import parse_regression_result, RegressionResult
from .core.formatter import ResultFormatter
from .exporters.xlsx_exporter import export_to_excel
from .exporters.docx_exporter import export_to_docx
from .utils.statistics import (
    compute_summary_statistics,
    compute_detailed_statistics, 
    compute_grouped_statistics,
    compute_cross_tabulation,
    format_statistics_for_export
)
from .utils.helpers import validate_filename, validate_regression_result


def outreg(model_result: Any = None,
          filename: Optional[str] = None,
          data: Optional[pd.DataFrame] = None,
          # File options
          replace: bool = False,
          append: bool = False,
          # Formatting options  
          dec: Optional[int] = None,
          bdec: Optional[int] = None,
          sdec: Optional[int] = None,
          # Variable selection
          keep: Optional[List[str]] = None,
          drop: Optional[List[str]] = None,
          # Labels and titles
          label: bool = False,
          ctitle: Optional[str] = None,
          title: Optional[str] = None,
          # Notes and content
          addnote: Optional[str] = None,
          nonotes: bool = False,
          addstat: Optional[Dict[str, Union[float, List[float]]]] = None,
          # Regression specific
          eform: bool = False,
          # Layout options
          landscape: bool = False,
          font_size: int = 11,
          font_name: str = "Times New Roman",
          # Statistics options
          include_nobs: bool = True,
          include_rsq: bool = True,
          include_fstat: bool = True,
          # Summary statistics mode
          sum_stats: bool = False,
          detail: bool = False,
          by: Optional[str] = None,
          # Cross-tabulation mode
          cross_tab: Optional[List[str]] = None,
          **kwargs) -> Optional[pd.DataFrame]:
    """
    Export regression results or statistics to Excel/Word files.
    
    This function replicates the functionality of Stata's outreg2 command,
    allowing you to export regression results from statsmodels and linearmodels
    to professional publication-quality tables.
    
    Parameters:
    -----------
    model_result : regression result object
        Fitted model result from statsmodels, linearmodels, etc.
    filename : str, optional
        Output filename (.xlsx or .docx). If None, returns DataFrame.
    data : pd.DataFrame, optional
        Data for summary statistics or cross-tabulation
    replace : bool, default False
        Replace existing file
    append : bool, default False
        Append to existing file
    dec : int, optional
        Overall decimal places
    bdec : int, optional
        Decimal places for coefficients
    sdec : int, optional  
        Decimal places for standard errors
    keep : List[str], optional
        Variables to keep in output
    drop : List[str], optional
        Variables to drop from output
    label : bool, default False
        Use variable labels if available
    ctitle : str, optional
        Column title for this model
    title : str, optional
        Table title
    addnote : str, optional
        Additional note to add
    nonotes : bool, default False
        Suppress all notes including significance stars
    addstat : Dict[str, float or List[float]], optional
        Additional statistics to include
    eform : bool, default False
        Report exponentiated coefficients (odds ratios)
    landscape : bool, default False
        Use landscape orientation (Word only)
    font_size : int, default 11
        Font size for output
    font_name : str, default "Times New Roman"
        Font name for output
    include_nobs : bool, default True
        Include number of observations
    include_rsq : bool, default True
        Include R-squared
    include_fstat : bool, default True
        Include F-statistic
    sum_stats : bool, default False
        Export summary statistics instead of regression
    detail : bool, default False
        Include detailed statistics (percentiles, etc.)
    by : str, optional
        Group variable for summary statistics
    cross_tab : List[str], optional
        Variables for cross-tabulation [var1, var2]
        
    Returns:
    --------
    pd.DataFrame or None
        Formatted table if filename is None, otherwise None
        
    Examples:
    ---------
    Basic regression export:
    >>> import statsmodels.api as sm
    >>> result = sm.OLS(y, X).fit()
    >>> outreg(result, 'regression.xlsx', replace=True)
    
    Multiple model comparison:
    >>> outreg(result1, 'comparison.xlsx', replace=True, ctitle='Model 1')
    >>> outreg(result2, 'comparison.xlsx', append=True, ctitle='Model 2')
    
    Summary statistics:
    >>> outreg(data=df, filename='stats.xlsx', sum_stats=True, replace=True)
    
    Cross-tabulation:
    >>> outreg(data=df, filename='crosstab.xlsx', 
    ...        cross_tab=['var1', 'var2'], replace=True)
    """
    
    # Parse options
    options = parse_options(
        replace=replace, append=append, dec=dec, bdec=bdec, sdec=sdec,
        keep=keep, drop=drop, label=label, ctitle=ctitle, title=title,
        addnote=addnote, nonotes=nonotes, addstat=addstat, eform=eform,
        landscape=landscape, font_size=font_size, font_name=font_name,
        include_nobs=include_nobs, include_rsq=include_rsq, 
        include_fstat=include_fstat, **kwargs
    )
    
    # Determine operation mode
    if cross_tab is not None:
        # Cross-tabulation mode
        if data is None:
            raise ValueError("Data must be provided for cross-tabulation")
        if len(cross_tab) != 2:
            raise ValueError("cross_tab must contain exactly 2 variables")
        
        result_df = compute_cross_tabulation(data, cross_tab[0], cross_tab[1], options)
        
    elif sum_stats:
        # Summary statistics mode
        if data is None:
            raise ValueError("Data must be provided for summary statistics")
        
        if by is not None:
            # Grouped statistics
            variables = keep if keep is not None else None
            result_df = compute_grouped_statistics(data, by, variables, options)
        elif detail:
            # Detailed statistics
            variables = keep if keep is not None else None
            result_df = compute_detailed_statistics(data, variables, options)
            result_df = format_statistics_for_export(result_df, options)
        else:
            # Basic summary statistics
            variables = keep if keep is not None else None
            result_df = compute_summary_statistics(data, variables, options)
            result_df = format_statistics_for_export(result_df, options)
            
    else:
        # Regression mode
        if model_result is None:
            raise ValueError("model_result must be provided for regression export")
        
        # Validate model result
        validate_regression_result(model_result)
        
        # Parse regression result
        parsed_result = parse_regression_result(model_result, ctitle)
        
        # Format results
        formatter = ResultFormatter(options)
        result_df = formatter.format_regression_table([parsed_result])
        
        # Add title and notes
        result_df = formatter.add_title_and_notes(result_df)
    
    # Export or return
    if filename is not None:
        # Validate filename
        filepath = validate_filename(filename)
        
        # Export based on file extension
        if filepath.suffix.lower() == '.xlsx':
            export_to_excel(result_df, str(filepath), options)
        elif filepath.suffix.lower() == '.docx':
            export_to_docx(result_df, str(filepath), options)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
        
        print(f"Results exported to {filepath}")
        return None
    else:
        return result_df


def summary_stats(data: pd.DataFrame,
                 filename: Optional[str] = None,
                 variables: Optional[List[str]] = None,
                 detail: bool = False,
                 by: Optional[str] = None,
                 **kwargs) -> Optional[pd.DataFrame]:
    """
    Convenience function for exporting summary statistics.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Input data
    filename : str, optional
        Output filename
    variables : List[str], optional
        Variables to include
    detail : bool, default False
        Include detailed statistics
    by : str, optional
        Group variable
    **kwargs
        Additional options for outreg()
        
    Returns:
    --------
    pd.DataFrame or None
        Summary statistics table
    """
    
    return outreg(
        data=data,
        filename=filename,
        keep=variables,
        sum_stats=True,
        detail=detail,
        by=by,
        **kwargs
    )


def cross_tab(data: pd.DataFrame,
             var1: str,
             var2: str,
             filename: Optional[str] = None,
             **kwargs) -> Optional[pd.DataFrame]:
    """
    Convenience function for exporting cross-tabulation.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Input data
    var1 : str
        Row variable
    var2 : str
        Column variable
    filename : str, optional
        Output filename
    **kwargs
        Additional options for outreg()
        
    Returns:
    --------
    pd.DataFrame or None
        Cross-tabulation table
    """
    
    return outreg(
        data=data,
        filename=filename,
        cross_tab=[var1, var2],
        **kwargs
    )


def outreg_compare(results: List[Any],
                  filename: Optional[str],
                  model_names: Optional[List[str]] = None,
                  **kwargs) -> Optional[pd.DataFrame]:
    """
    Compare multiple regression models in a single table.
    
    Parameters:
    -----------
    results : List[Any]
        List of regression result objects
    filename : str or None
        Output filename. If None, returns DataFrame instead of saving
    model_names : List[str], optional
        Names for each model
    **kwargs
        Additional options for outreg()
        
    Returns:
    --------
    pd.DataFrame or None
        Comparison table if filename is None, otherwise None
    """
    
    if not results:
        raise ValueError("No results provided")
    
    # Parse options
    options = parse_options(**kwargs)
    
    # Parse all results
    parsed_results = []
    for i, result in enumerate(results):
        name = model_names[i] if model_names and i < len(model_names) else f"Model {i+1}"
        parsed_results.append(parse_regression_result(result, name))
    
    # Format results
    formatter = ResultFormatter(options)
    result_df = formatter.format_regression_table(parsed_results)
    result_df = formatter.add_title_and_notes(result_df)
    
    # Export or return
    if filename is not None:
        # Export to file
        filepath = validate_filename(filename)
        
        if filepath.suffix.lower() == '.xlsx':
            export_to_excel(result_df, str(filepath), options)
        elif filepath.suffix.lower() == '.docx':
            export_to_docx(result_df, str(filepath), options)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
        
        print(f"Comparison table exported to {filepath}")
        return None
    else:
        # Return DataFrame
        return result_df


# Aliases for convenience
outreg2 = outreg  # For users familiar with Stata
export_regression = outreg
export_stats = summary_stats
export_crosstab = cross_tab
