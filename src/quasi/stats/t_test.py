from scipy.stats import t as tdist
import statsmodels.api as sm
import numpy as np
import pandas as pd

''' This follows the methodology set out by Dalheim and Steen (2020)
Dalheim, , Steen, S.: A computationally efficient method for identification of
steady state in time series data from ship monitoring. Journal of Ocean En
gineering and Science 5(4), 333–345 (2020) https://doi.org/10.1016/j.joes.
2020.01.003'''


def t_test_window_time(time_array):

    window_time = time_array - min(time_array)

    return window_time



def calc_b1_hat(data_array,
                window_time):

    n = len(data_array)
    xy_sum = np.dot(data_array, window_time)
    # linear slope b1_hat estimated by ordinary least squares estimation
    b1_hat = ((sum(x * y for x, y in list(zip(data_array, window_time))) - (1/n)*sum(data_array)*sum(window_time)) /
              (sum(window_time**2) - (1/n)*(sum(window_time)**2)))

    return b1_hat



def calc_b0_hat(data_array,
                b1_hat,
                window_time):

    n = len(data_array)
    # Intercept estimate by subtracting estimated linear drift component b1_hat * t from window_data
    b0_hat = (1/n) * (sum(data_array) - b1_hat * sum(window_time))

    return b0_hat



def calc_sigmaa_hat(b1_hat,
                    b0_hat,
                    data_array):

    n = len(data_array)
    # White noise standard deviation
    sigmaa_hat = np.sqrt((1/(n-2)) * sum((x - b1_hat - b0_hat)**2 for x in data_array))

    return sigmaa_hat



def calc_sigmab1_hat(sigmaa_hat,
                     window_time):

    # standard deviation of estimated slope
    sigmab1_hat = sigmaa_hat / np.sqrt(sum((window_time - np.mean(window_time))**2))

    return sigmab1_hat



def calc_t_value(b1_hat, sigmab1_hat):

    t1 = b1_hat / sigmab1_hat

    return t1



def calc_critical_t_value(alpha,
                          dof):

    ct_value = tdist.ppf(1 - alpha/2, dof - 2)

    return ct_value



def t_test(data_array,
           time_array,
           alpha=0.025,
           value_to_return='steady_result'):

    window_time = t_test_window_time(time_array)
    b1_hat = calc_b1_hat(data_array, window_time)
    b0_hat = calc_b0_hat(data_array, b1_hat, window_time)
    sigmaa_hat = calc_sigmaa_hat(b1_hat, b0_hat, data_array)
    sigmab1_hat = calc_sigmab1_hat(sigmaa_hat, window_time)
    t_value = calc_t_value(b1_hat, sigmab1_hat)

    # Now to check for the null-hypothesis, alpha is the confidence level that is set in the function
    critical_t_value = calc_critical_t_value(alpha, len(data_array))

    test = abs(t_value)/critical_t_value

    if test >= 1:
        steady = 0

    else:
        steady = 1

    values_to_return = {'b1_hat': b1_hat, 
                        'b0_hat': b0_hat, 
                        'sigmaa_hat': sigmaa_hat, 
                        'sigmab1_hat': sigmab1_hat, 
                        'steady_result': steady, 
                        't-value': t_value}

    if value_to_return not in values_to_return:
        raise ValueError(f"Invalid sim type. Expected one of: {values_to_return.keys()}")

    return values_to_return[value_to_return]



if (__name__ == '__main__'):
    sunspots = sm.datasets.sunspots.load_pandas().data

    sunspots.index = pd.Index(sm.tsa.datetools.dates_from_range("1700", "2008"))

    result = t_test(sunspots["SUNACTIVITY"], sunspots['YEAR'])

    print(f't-test results: {result}')