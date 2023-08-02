import pandas as pd
import numpy as np

from typing import Optional

SCALING_FACTOR_CONSUMPTION = 20 * 2900 / 5e+08

def scale_solar(df:pd.DataFrame,solar_col_name:str,solar_capacity:float) -> None:
    # normalize the solar data so the max output is 1
    df[solar_col_name] = df[solar_col_name] * solar_capacity / 10770 #df[solar_col_name].max() The max no longer works with the np.arrays as values in the cells
    # multiply by installed capacity so it peaks at around the installed capacity
    #df[solar_col_name] *= solar_capacity

def scale_consumption(df:pd.DataFrame,consumption_col_name:str,scaling_factor_consumption:float) -> None:
    df[consumption_col_name] = df[consumption_col_name] * scaling_factor_consumption