"""
Statistical utilities for pyoutreg.
Provides summary statistics and cross-tabulation functionality.
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any, Union
from ..core.options import OutregOptions


def compute_summary_statistics(data: pd.DataFrame, 
                             variables: Optional[List[str]] = None,
                             options: Optional[OutregOptions] = None) -> pd.DataFrame:
    """
    Compute summary statistics similar to Stata's summarize command.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Input data
    variables : List[str], optional
        Variables to include. If None, all numeric variables are used.
    options : OutregOptions, optional
        Options for formatting and variable selection
        
    Returns:
    --------
    pd.DataFrame
        Summary statistics table
    """
    
    if options is None:
        options = OutregOptions()
    
    # Select variables
    if variables is None:
        variables = list(data.select_dtypes(include=[np.number]).columns)
    
    # Apply keep/drop filters
    if options.keep is not None:
        variables = [v for v in variables if v in options.keep]
    elif options.drop is not None:
        variables = [v for v in variables if v not in options.drop]
    
    # Remove variables not in data
    variables = [v for v in variables if v in data.columns]
    
    if not variables:
        raise ValueError("No valid variables found for summary statistics")
    
    # Compute statistics
    summary_data = []
    
    for var in variables:
        if var in data.columns:
            series = data[var].dropna()
            
            if len(series) == 0:
                continue
                
            stats = {
                'Variable': var,
                'N': len(series),
                'Mean': series.mean(),
                'Std Dev': series.std(),
                'Min': series.min(),
                'Max': series.max()
            }
            
            summary_data.append(stats)
    
    return pd.DataFrame(summary_data)


def compute_detailed_statistics(data: pd.DataFrame, 
                               variables: Optional[List[str]] = None,
                               options: Optional[OutregOptions] = None) -> pd.DataFrame:
    """
    Compute detailed summary statistics including percentiles.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Input data
    variables : List[str], optional
        Variables to include
    options : OutregOptions, optional
        Options for formatting and variable selection
        
    Returns:
    --------
    pd.DataFrame
        Detailed summary statistics table
    """
    
    if options is None:
        options = OutregOptions()
    
    # Select variables
    if variables is None:
        variables = list(data.select_dtypes(include=[np.number]).columns)
    
    # Apply keep/drop filters  
    if options.keep is not None:
        variables = [v for v in variables if v in options.keep]
    elif options.drop is not None:
        variables = [v for v in variables if v not in options.drop]
    
    # Remove variables not in data
    variables = [v for v in variables if v in data.columns]
    
    if not variables:
        raise ValueError("No valid variables found for detailed statistics")
    
    # Compute detailed statistics
    detail_data = []
    
    for var in variables:
        if var in data.columns:
            series = data[var].dropna()
            
            if len(series) == 0:
                continue
            
            stats = {
                'Variable': var,
                'N': len(series),
                'Mean': series.mean(),
                'Std Dev': series.std(),
                'Skewness': series.skew(),
                'Kurtosis': series.kurtosis(),
                'Min': series.min(),
                'P1': series.quantile(0.01),
                'P5': series.quantile(0.05),
                'P10': series.quantile(0.10),
                'P25': series.quantile(0.25),
                'P50': series.quantile(0.50),
                'P75': series.quantile(0.75),
                'P90': series.quantile(0.90),
                'P95': series.quantile(0.95),
                'P99': series.quantile(0.99),
                'Max': series.max()
            }
            
            detail_data.append(stats)
    
    return pd.DataFrame(detail_data)


def compute_grouped_statistics(data: pd.DataFrame, 
                             group_var: str,
                             variables: Optional[List[str]] = None,
                             options: Optional[OutregOptions] = None) -> pd.DataFrame:
    """
    Compute summary statistics by group.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Input data
    group_var : str
        Variable to group by
    variables : List[str], optional
        Variables to include in statistics
    options : OutregOptions, optional
        Options for formatting and variable selection
        
    Returns:
    --------
    pd.DataFrame
        Grouped summary statistics table
    """
    
    if options is None:
        options = OutregOptions()
    
    if group_var not in data.columns:
        raise ValueError(f"Group variable '{group_var}' not found in data")
    
    # Select variables
    if variables is None:
        variables = list(data.select_dtypes(include=[np.number]).columns)
        # Remove group variable if it's numeric
        if group_var in variables:
            variables.remove(group_var)
    
    # Apply keep/drop filters
    if options.keep is not None:
        variables = [v for v in variables if v in options.keep]
    elif options.drop is not None:
        variables = [v for v in variables if v not in options.drop]
    
    # Remove variables not in data
    variables = [v for v in variables if v in data.columns]
    
    if not variables:
        raise ValueError("No valid variables found for grouped statistics")
    
    # Compute grouped statistics
    grouped_data = []
    
    for group_value in sorted(data[group_var].unique()):
        if pd.isna(group_value):
            continue
            
        group_data = data[data[group_var] == group_value]
        
        for var in variables:
            if var in group_data.columns:
                series = group_data[var].dropna()
                
                if len(series) == 0:
                    continue
                
                stats = {
                    'Group': f"{group_var}={group_value}",
                    'Variable': var,
                    'N': len(series),
                    'Mean': series.mean(),
                    'Std Dev': series.std(),
                    'Min': series.min(),
                    'Max': series.max()
                }
                
                grouped_data.append(stats)
    
    return pd.DataFrame(grouped_data)


def compute_cross_tabulation(data: pd.DataFrame, 
                           var1: str, 
                           var2: str,
                           options: Optional[OutregOptions] = None) -> pd.DataFrame:
    """
    Compute cross-tabulation table.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Input data
    var1 : str
        First variable (rows)
    var2 : str
        Second variable (columns)
    options : OutregOptions, optional
        Options for formatting
        
    Returns:
    --------
    pd.DataFrame
        Cross-tabulation table with counts and percentages
    """
    
    if options is None:
        options = OutregOptions()
    
    if var1 not in data.columns:
        raise ValueError(f"Variable '{var1}' not found in data")
    if var2 not in data.columns:
        raise ValueError(f"Variable '{var2}' not found in data")
    
    # Create cross-tabulation
    crosstab = pd.crosstab(data[var1], data[var2], margins=True, margins_name="Total")
    
    # Convert to percentage (column percentages)
    crosstab_pct = pd.crosstab(data[var1], data[var2], normalize='columns') * 100
    
    # Combine counts and percentages
    result_data = []
    
    # Header row
    header = [f"{var1}\\{var2}"] + [str(col) for col in crosstab.columns]
    result_data.append(header)
    
    # Data rows
    for row_name in crosstab.index:
        row_data = [str(row_name)]
        
        for col_name in crosstab.columns:
            if col_name == "Total":
                # For total column, just show counts
                cell_value = str(crosstab.loc[row_name, col_name])
            else:
                # For data cells, show count (percentage)
                count = crosstab.loc[row_name, col_name]
                if row_name != "Total" and col_name in crosstab_pct.columns:
                    pct = crosstab_pct.loc[row_name, col_name]
                    cell_value = f"{count} ({pct:.1f}%)"
                else:
                    cell_value = str(count)
            
            row_data.append(cell_value)
        
        result_data.append(row_data)
    
    # Convert to DataFrame
    df = pd.DataFrame(result_data[1:], columns=result_data[0])
    
    return df


def format_statistics_for_export(stats_df: pd.DataFrame, 
                                options: OutregOptions) -> pd.DataFrame:
    """
    Format statistics DataFrame for export with proper decimal places.
    
    Parameters:
    -----------
    stats_df : pd.DataFrame
        Statistics DataFrame
    options : OutregOptions
        Formatting options
        
    Returns:
    --------
    pd.DataFrame
        Formatted DataFrame ready for export
    """
    
    formatted_df = stats_df.copy()
    
    # Columns that should be formatted as numbers
    numeric_cols = ['Mean', 'Std Dev', 'Min', 'Max', 'Skewness', 'Kurtosis']
    percentile_cols = [col for col in stats_df.columns if col.startswith('P')]
    numeric_cols.extend(percentile_cols)
    
    # Apply formatting
    for col in numeric_cols:
        if col in formatted_df.columns:
            formatted_df[col] = formatted_df[col].apply(
                lambda x: f"{x:.{options.bdec}f}" if pd.notna(x) else ''
            )
    
    # Format N as integer
    if 'N' in formatted_df.columns:
        formatted_df['N'] = formatted_df['N'].apply(
            lambda x: str(int(x)) if pd.notna(x) else ''
        )
    
    return formatted_df
