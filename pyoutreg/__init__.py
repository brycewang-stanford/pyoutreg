"""
PyOutreg: A Python implementation of Stata's outreg2 command.

This package provides functionality to export regression results from 
statsmodels and linearmodels to Excel and Word formats with professional
publication-quality formatting.
"""

from .outreg import outreg, summary_stats, cross_tab, outreg_compare

__version__ = "0.1.0"
__author__ = "Bryce Wang"
__email__ = "brycewang@example.com"

__all__ = ["outreg", "summary_stats", "cross_tab", "outreg_compare"]
