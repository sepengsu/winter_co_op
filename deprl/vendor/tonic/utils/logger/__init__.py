from myutils import logger

__all__ = [name for name in dir(logger) if not (name.startswith("_") and name=='MyLogger')]