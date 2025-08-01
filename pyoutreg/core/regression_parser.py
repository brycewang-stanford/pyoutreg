"""
Regression result parser for different model types.
Extracts coefficients, standard errors, and statistics from various regression models.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Union
import warnings

# Import statements with error handling
try:
    import statsmodels.api as sm
    from statsmodels.base.model import Results as StatsResults
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False
    StatsResults = None

try:
    import linearmodels
    from linearmodels.panel.results import PanelResults
    from linearmodels.iv.results import IVResults
    HAS_LINEARMODELS = True
except ImportError:
    HAS_LINEARMODELS = False
    PanelResults = None
    IVResults = None


class RegressionResult:
    """Standardized container for regression results."""
    
    def __init__(self, model_type: str, coefficients: pd.Series, 
                 std_errors: pd.Series, tvalues: pd.Series, 
                 pvalues: pd.Series, statistics: Dict[str, Any],
                 nobs: int, model_name: Optional[str] = None):
        self.model_type = model_type
        self.coefficients = coefficients
        self.std_errors = std_errors
        self.tvalues = tvalues
        self.pvalues = pvalues
        self.statistics = statistics
        self.nobs = nobs
        self.model_name = model_name or model_type
        
    @property
    def param_names(self) -> List[str]:
        """Get parameter names."""
        return list(self.coefficients.index)
    
    def get_confidence_interval(self, alpha: float = 0.05) -> pd.DataFrame:
        """Calculate confidence intervals."""
        from scipy import stats
        t_crit = stats.t.ppf(1 - alpha/2, self.nobs - len(self.coefficients))
        margin = t_crit * self.std_errors
        
        return pd.DataFrame({
            'lower': self.coefficients - margin,
            'upper': self.coefficients + margin
        }, index=self.coefficients.index)


class RegressionParser:
    """Parser for different types of regression results."""
    
    @staticmethod
    def parse(result: Any, model_name: Optional[str] = None) -> RegressionResult:
        """Parse regression result based on its type."""
        
        module_name = result.__class__.__module__
        
        if HAS_STATSMODELS and 'statsmodels' in module_name:
            return RegressionParser._parse_statsmodels(result, model_name)
        elif HAS_LINEARMODELS and 'linearmodels' in module_name:
            return RegressionParser._parse_linearmodels(result, model_name)
        else:
            raise TypeError(f"Unsupported model type: {type(result)}")
    
    @staticmethod
    def _parse_statsmodels(result: Any, model_name: Optional[str] = None) -> RegressionResult:
        """Parse statsmodels results."""
        
        # Determine model type from underlying model
        if hasattr(result, 'model'):
            model_class = result.model.__class__.__name__
        else:
            model_class = result.__class__.__name__
            
        if 'OLS' in model_class:
            model_type = 'OLS'
        elif 'Logit' in model_class:
            model_type = 'Logit'
        elif 'Probit' in model_class:
            model_type = 'Probit'
        elif 'GLM' in model_class:
            model_type = 'GLM'
        else:
            # Check result class name as fallback
            result_class = result.__class__.__name__
            if 'Binary' in result_class:
                model_type = 'Logit'
            elif 'Regression' in result_class:
                model_type = 'OLS'
            else:
                model_type = 'Regression'
        
        # Extract basic results
        coefficients = result.params
        std_errors = result.bse
        tvalues = result.tvalues
        pvalues = result.pvalues
        nobs = int(result.nobs)
        
        # Extract model statistics
        statistics = {
            'rsquared': getattr(result, 'rsquared', None),
            'rsquared_adj': getattr(result, 'rsquared_adj', None),
            'fvalue': getattr(result, 'fvalue', None),
            'f_pvalue': getattr(result, 'f_pvalue', None),
            'aic': getattr(result, 'aic', None),
            'bic': getattr(result, 'bic', None),
            'llf': getattr(result, 'llf', None),
        }
        
        # Model-specific statistics
        if model_type in ['Logit', 'Probit']:
            statistics.update({
                'pseudo_rsquared': getattr(result, 'prsquared', None),
                'llr': getattr(result, 'llr', None),
                'llr_pvalue': getattr(result, 'llr_pvalue', None),
            })
        
        return RegressionResult(
            model_type=model_type,
            coefficients=coefficients,
            std_errors=std_errors,
            tvalues=tvalues,
            pvalues=pvalues,
            statistics=statistics,
            nobs=nobs,
            model_name=model_name
        )
    
    @staticmethod
    def _parse_linearmodels(result: Any,
                          model_name: Optional[str] = None) -> RegressionResult:
        """Parse linearmodels results."""
        
        # Determine model type
        if isinstance(result, PanelResults):
            if hasattr(result, 'entity_effects') and result.entity_effects:
                model_type = 'Fixed Effects'
            elif hasattr(result, 'random_effects') and result.random_effects:
                model_type = 'Random Effects'
            else:
                model_type = 'Panel OLS'
        elif isinstance(result, IVResults):
            model_type = 'IV Regression'
        else:
            model_type = 'Panel Regression'
        
        # Extract basic results
        coefficients = result.params
        std_errors = result.std_errors
        tvalues = result.tstats
        pvalues = result.pvalues
        nobs = int(result.nobs)
        
        # Extract model statistics
        statistics = {
            'rsquared': getattr(result, 'rsquared', None),
            'rsquared_adj': getattr(result, 'rsquared_adj', None),
            'fvalue': getattr(result, 'fstat', None),
            'f_pvalue': getattr(result, 'f_pvalue', None),
        }
        
        # Panel-specific statistics
        if isinstance(result, PanelResults):
            statistics.update({
                'rsquared_within': getattr(result, 'rsquared_within', None),
                'rsquared_between': getattr(result, 'rsquared_between', None),
                'rsquared_overall': getattr(result, 'rsquared_overall', None),
            })
        
        # IV-specific statistics
        if isinstance(result, IVResults):
            statistics.update({
                'j_stat': getattr(result, 'j_stat', None),
                'j_pvalue': getattr(result, 'j_pvalue', None),
                'first_stage_fstat': getattr(result, 'first_stage', {}).get('fstat', None),
            })
        
        return RegressionResult(
            model_type=model_type,
            coefficients=coefficients,
            std_errors=std_errors,
            tvalues=tvalues,
            pvalues=pvalues,
            statistics=statistics,
            nobs=nobs,
            model_name=model_name
        )


def parse_regression_result(result: Any, model_name: Optional[str] = None) -> RegressionResult:
    """Convenience function to parse regression results."""
    return RegressionParser.parse(result, model_name)
