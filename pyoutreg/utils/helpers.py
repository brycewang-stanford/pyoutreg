"""
Helper utilities for pyoutreg.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, List, Optional, Any, Dict
import warnings


def validate_filename(filename: Union[str, Path], 
                     supported_formats: List[str] = ['.xlsx', '.docx']) -> Path:
    """
    Validate and normalize filename.
    
    Parameters:
    -----------
    filename : str or Path
        Output filename
    supported_formats : List[str]
        List of supported file extensions
        
    Returns:
    --------
    Path
        Validated Path object
        
    Raises:
    -------
    ValueError
        If file extension is not supported
    """
    
    filepath = Path(filename)
    
    if filepath.suffix.lower() not in supported_formats:
        raise ValueError(f"Unsupported file format: {filepath.suffix}. "
                        f"Supported formats: {', '.join(supported_formats)}")
    
    # Create directory if it doesn't exist
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    return filepath


def detect_model_type(model_result: Any) -> str:
    """
    Detect the type of regression model from the result object.
    
    Parameters:
    -----------
    model_result : Any
        Model result object
        
    Returns:
    --------
    str
        Model type string
    """
    
    model_class = model_result.__class__.__name__
    module_name = model_result.__class__.__module__
    
    # Handle statsmodels
    if 'statsmodels' in module_name:
        # Check if it's a wrapper - get the underlying model
        if hasattr(model_result, 'model'):
            underlying_model = model_result.model.__class__.__name__
            if 'OLS' in underlying_model:
                return 'OLS'
            elif 'Logit' in underlying_model:
                return 'Logit'
            elif 'Probit' in underlying_model:
                return 'Probit'
            elif 'GLM' in underlying_model:
                return 'GLM'
        
        # Fallback to checking result class name
        if 'OLS' in model_class or 'Regression' in model_class:
            return 'OLS'
        elif 'Logit' in model_class or 'Binary' in model_class:
            return 'Logit'
        elif 'Probit' in model_class:
            return 'Probit'
        elif 'GLM' in model_class:
            return 'GLM'
        else:
            return 'Statsmodels Regression'
    
    # Handle linearmodels
    elif 'linearmodels' in module_name:
        if 'Panel' in model_class:
            return 'Panel Regression'
        elif 'IV' in model_class:
            return 'IV Regression'
        else:
            return 'Linear Models Regression'
    
    else:
        return 'Unknown Regression'


def clean_variable_names(names: List[str]) -> List[str]:
    """
    Clean variable names for output display.
    
    Parameters:
    -----------
    names : List[str]
        Variable names to clean
        
    Returns:
    --------
    List[str]
        Cleaned variable names
    """
    
    cleaned = []
    for name in names:
        # Remove common prefixes/suffixes that might be added by models
        clean_name = str(name).strip()
        
        # Replace underscores with spaces for better readability
        if '_' in clean_name and len(clean_name.split('_')) <= 3:
            clean_name = clean_name.replace('_', ' ')
        
        # Capitalize first letter
        if clean_name and clean_name[0].islower():
            clean_name = clean_name[0].upper() + clean_name[1:]
        
        cleaned.append(clean_name)
    
    return cleaned


def merge_options(default_options: Dict[str, Any], 
                 user_options: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge user options with default options.
    
    Parameters:
    -----------
    default_options : Dict[str, Any]
        Default option values
    user_options : Dict[str, Any]
        User-provided options
        
    Returns:
    --------
    Dict[str, Any]
        Merged options dictionary
    """
    
    merged = default_options.copy()
    merged.update(user_options)
    return merged


def check_data_compatibility(data: pd.DataFrame, 
                           required_columns: Optional[List[str]] = None) -> bool:
    """
    Check if data is compatible with pyoutreg operations.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Input data
    required_columns : List[str], optional
        Columns that must be present
        
    Returns:
    --------
    bool
        True if data is compatible
        
    Raises:
    -------
    ValueError
        If data is incompatible
    """
    
    if data.empty:
        raise ValueError("Data is empty")
    
    if required_columns:
        missing_cols = [col for col in required_columns if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
    
    return True


def handle_missing_values(data: pd.DataFrame, 
                         strategy: str = 'ignore') -> pd.DataFrame:
    """
    Handle missing values in data.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Input data
    strategy : str
        Strategy for handling missing values:
        - 'ignore': Keep as is
        - 'drop': Drop rows with any missing values
        - 'warn': Issue warning about missing values
        
    Returns:
    --------
    pd.DataFrame
        Data with missing values handled
    """
    
    if strategy == 'ignore':
        return data
    
    elif strategy == 'drop':
        n_before = len(data)
        data_clean = data.dropna()
        n_after = len(data_clean)
        
        if n_after < n_before:
            warnings.warn(f"Dropped {n_before - n_after} rows with missing values")
        
        return data_clean
    
    elif strategy == 'warn':
        missing_count = data.isnull().sum().sum()
        if missing_count > 0:
            warnings.warn(f"Data contains {missing_count} missing values")
        
        return data
    
    else:
        raise ValueError(f"Unknown missing value strategy: {strategy}")


def format_model_name(model_result: Any, user_name: Optional[str] = None) -> str:
    """
    Generate a formatted model name for display.
    
    Parameters:
    -----------
    model_result : Any
        Model result object
    user_name : str, optional
        User-provided name
        
    Returns:
    --------
    str
        Formatted model name
    """
    
    if user_name:
        return user_name
    
    model_type = detect_model_type(model_result)
    
    # Add sample size info if available
    if hasattr(model_result, 'nobs'):
        return f"{model_type} (N={int(model_result.nobs)})"
    else:
        return model_type


def get_variable_labels(data: pd.DataFrame) -> Dict[str, str]:
    """
    Extract variable labels from DataFrame attributes if available.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Input data
        
    Returns:
    --------
    Dict[str, str]
        Dictionary mapping variable names to labels
    """
    
    labels = {}
    
    # Check if DataFrame has labels attribute (some pandas extensions support this)
    if hasattr(data, 'labels'):
        labels.update(data.labels)
    
    # Check individual series for label attributes
    for col in data.columns:
        if hasattr(data[col], 'label') and data[col].label:
            labels[col] = data[col].label
        elif hasattr(data[col], 'attrs') and 'label' in data[col].attrs:
            labels[col] = data[col].attrs['label']
    
    return labels


def create_comparison_table(results_list: List[Any], 
                          model_names: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Create a side-by-side comparison table for multiple regression results.
    
    Parameters:
    -----------
    results_list : List[Any]
        List of regression result objects
    model_names : List[str], optional
        Names for each model
        
    Returns:
    --------
    pd.DataFrame
        Comparison table
    """
    
    from ..core.regression_parser import parse_regression_result
    
    parsed_results = []
    for i, result in enumerate(results_list):
        name = model_names[i] if model_names and i < len(model_names) else None
        parsed_results.append(parse_regression_result(result, name))
    
    # This function would need to be implemented to create the comparison
    # For now, return a placeholder
    return pd.DataFrame({'Message': ['Comparison table not yet implemented']})


def validate_regression_result(result: Any) -> bool:
    """
    Validate that result is a supported regression result object.
    
    Parameters:
    -----------
    result : Any
        Regression result object to validate
        
    Returns:
    --------
    bool
        True if valid regression result
        
    Raises:
    -------
    TypeError
        If result is not a valid regression result
    """
    
    # Check for statsmodels attributes
    statsmodels_attrs = ['params', 'bse', 'tvalues', 'pvalues']
    has_statsmodels_attrs = all(hasattr(result, attr) for attr in statsmodels_attrs)
    
    # Check for linearmodels attributes  
    linearmodels_attrs = ['params', 'std_errors', 'tstats', 'pvalues']
    has_linearmodels_attrs = all(hasattr(result, attr) for attr in linearmodels_attrs)
    
    if not (has_statsmodels_attrs or has_linearmodels_attrs):
        # Determine which attributes are missing for better error message
        if hasattr(result, 'params'):
            missing_attrs = []
            if not hasattr(result, 'bse') and not hasattr(result, 'std_errors'):
                missing_attrs.append('bse or std_errors')
            if not hasattr(result, 'tvalues') and not hasattr(result, 'tstats'):
                missing_attrs.append('tvalues or tstats')
            if not hasattr(result, 'pvalues'):
                missing_attrs.append('pvalues')
            
            if missing_attrs:
                raise TypeError(f"Result object missing required attributes: {', '.join(missing_attrs)}")
        else:
            raise TypeError("Result object missing required attribute: params")
    
    return True
