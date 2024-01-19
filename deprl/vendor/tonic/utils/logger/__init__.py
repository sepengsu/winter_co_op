import inspect
from myutils import logger

functions = [name for name, value in inspect.getmembers(logger) 
             if inspect.isfunction(value) and not inspect.ismodule(value) and not inspect.isclass(value)]

globals().update({name: getattr(logger, name) for name in functions})

__all__ = functions