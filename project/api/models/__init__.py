'''
Import all models here.

Instead of having a models.py file, we can define a module
with separate files which are then imported, as done here.

Django uses "project.api.models", so this will work anyway.

Example usage:
    from .[model_name] import *
'''

from .shop import *

from .price import *