import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import pandas as pd

def adf_test(timeseries, significance_level):
    # allowable_significance_levels = [1, 5, 10]
    # if significance_level not in allowable_significance_levels:
    #     raise ValueError('significance_level must be in [1, 5, 10] %')

    allowable_significance_levels = [1, 5, 10]

    if significance_level not in allowable_significance_levels:
        raise ValueError(f"Critical must be one of: {allowable_significance_levels}")

    dftest = adfuller(timeseries, autolag="AIC")
    index_of_critical_values = 4

    t_value = dftest[0]
    crit_value = dftest[index_of_critical_values][f"{crit_value}%"]

    if t_value < crit_value:
        return 1

    elif t_value > crit_value:
        return 0



if (__name__ == '__main__'):
    sunspots = sm.datasets.sunspots.load_pandas().data

    sunspots.index = pd.Index(sm.tsa.datetools.dates_from_range("1700", "2008"))
    del sunspots["YEAR"]

    result = adf_test(sunspots["SUNACTIVITY"], crit_value=10)

    print(f'ADF test results: {result}')