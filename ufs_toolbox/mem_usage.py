import pandas as pd


def mem_usage(pandas_obj):
    """
    Returns memory usage of pandas dataframe
    """
    usage = pandas_obj.memory_usage(deep=True)
    # we assume if not a df it's a series
    usage_b = usage.sum() if isinstance(pandas_obj, pd.DataFrame) else usage
    return usage_b / 1024 ** 2  # convert bytes to megabytes
