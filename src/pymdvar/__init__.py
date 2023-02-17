from typing import Any
from .pymdvar import VariableExtension

__all__ = ['VariableExtension']


# this should be in pymdvar.py, but since there is only one extension,
#  it is fine in here
def makeExtension(*args: Any, **kwargs: Any):
    return VariableExtension(*args, **kwargs)
