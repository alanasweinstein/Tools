#!/usr/bin/env python
"""
Debugger recipes from Ch. 3 of Wes McKinney's Python for Data Analysis (First Edition). Recipes and descriptions are copied verbatim. 
"""

def set_trace():
    """
    Put `set_trace()` anywhere in your code that you want to stop and take a look around (e.g., right before an exception occurs).
    Pressing `c` (continue) will cause the code to resume normally with no harm done.
    """
    from IPython.core.debugger import Pdb
    pdb = Pdb(color_scheme='Linux').set_trace(sys._getframe().f_back)
    

def debug(f, *args, **kwargs):
    """
    Enables you to invoke the interactive debugger easily on an arbitrary functional call.
    Example: suppose we had written a function like 
    `def f(x, y, z=1):
        tmp = x + y
        return tmp/z`
    and we wish to step through its logic. Ordinarily using `f` would look like `f(1, 2, z=3)`.
    To instead step into `f`, pass `f` as the first argument to `debug` followed by the positional and keyword arguments to be passed to `f`:
        `debug(f, 1, 2, z=3)`
    """
    from IPython.core.debugger import Pdb
    pdb = Pdb(color_scheme='Linux')
    return pdb.runcall(f, *args, **kwargs)
    
