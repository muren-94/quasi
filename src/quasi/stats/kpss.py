import statsmodels.api as sm
from statsmodels.tsa.stattools import kpss
import pandas as pd

def kpss_test(timeseries, significance_level):
    
    allowable_significance_levels = [1, 5, 10]

    if significance_level not in allowable_significance_levels:
        raise ValueError(f"Significance level (%) must be one of: {allowable_significance_levels}")
    
    dftest = kpss(timeseries, regression="c", nlags="auto")
    index_of_critical_values = 3

    t_value = dftest[0]
    crit_value = dftest[index_of_critical_values][f"{significance_level}%"]

    if t_value < crit_value:
        return 1

    elif t_value > crit_value:
        return 0
    

if (__name__ == '__main__'):
    sunspots = sm.datasets.sunspots.load_pandas().data

    sunspots.index = pd.Index(sm.tsa.datetools.dates_from_range("1700", "2008"))
    del sunspots["YEAR"]

    result = kpss_test(sunspots["SUNACTIVITY"], 5)

    print(f'KPSS test results: {result}')