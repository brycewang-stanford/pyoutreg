"""
Configuration and options management for pyoutreg.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union


@dataclass
class OutregOptions:
    """Configuration options for outreg output."""
    
    # File options
    replace: bool = False
    append: bool = False
    
    # Formatting options
    dec: Optional[int] = None  # Overall decimal places
    bdec: Optional[int] = None  # Coefficient decimal places  
    sdec: Optional[int] = None  # Standard error decimal places
    
    # Variable selection
    keep: Optional[List[str]] = None
    drop: Optional[List[str]] = None
    
    # Labels and titles
    label: bool = False
    ctitle: Optional[str] = None
    title: Optional[str] = None
    
    # Notes and additional content
    addnote: Optional[str] = None
    nonotes: bool = False
    addstat: Optional[Dict[str, float]] = None
    
    # Regression specific
    eform: bool = False  # For odds ratios in logit
    
    # Layout options
    landscape: bool = False
    font_size: int = 11
    font_name: str = "Times New Roman"
    
    # Statistics to include
    include_nobs: bool = True
    include_rsq: bool = True
    include_fstat: bool = True
    
    def __post_init__(self):
        """Validate and set default options."""
        if self.dec is not None:
            if self.bdec is None:
                self.bdec = self.dec
            if self.sdec is None:
                self.sdec = self.dec
        else:
            if self.bdec is None:
                self.bdec = 3
            if self.sdec is None:
                self.sdec = 3
                
        # Handle mutual exclusivity
        if self.replace and self.append:
            raise ValueError("Cannot specify both 'replace' and 'append'")
            
        if self.keep is not None and self.drop is not None:
            raise ValueError("Cannot specify both 'keep' and 'drop'")


def parse_options(**kwargs) -> OutregOptions:
    """Parse keyword arguments into OutregOptions."""
    return OutregOptions(**kwargs)
