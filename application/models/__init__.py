"""
While __init__ files are typically left empty, in this case, the __init__
file must make a relative import for each of the models -- inside .py files
-- to make them visible to the app. For example, if the menus.py file
contains the Breakfast model class, the __init__ file must declare the line
from .menus import Breakfast. This one-line syntax -- from .<file> import
<model_class> -- must be used in __init__.py for every model declared in .py
files inside the models folder.
"""
