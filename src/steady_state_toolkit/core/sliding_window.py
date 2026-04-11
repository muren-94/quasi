import numpy as np
from steady_state_toolkit import stats, plotting



def sliding_window_test(time_data,
                          test_data,
                          alpha=0.025,
                          window_size=50e-6,
                          sampling_rate=4e-7,
                          print_diagnostics=False,
                          save_t_test_matrix=False,
                          value_to_return='steady_result',
                          test_type='t_test'):

    # Performs the sliding window t-test assessment on a time data series and finds the average
    # steadiness of each sample in the series dependent on user defined window size and significance level

    # converts window size in microseconds to number of data points
    if print_diagnostics:
        print("Window size / sampling rate before rounding: ", window_size/sampling_rate)
    window_size = round(window_size / sampling_rate)

    # creates an arbitrary time array for the time series being evaluated
    time = np.arange(0, len(time_data), 1)

    if print_diagnostics:
        print("Window size after rounding: ", window_size)

    if window_size < 3:
        if print_diagnostics:
            print("Window size is too small, prescribing a value of 3 data points")
        window_size = 3

    # creates an empty 2D array for the steady data test results to be stored in
    steady_matrix = np.zeros((len(test_data) - window_size + 1, np.size(test_data)))

    # loops through the time series provided and performs the t_test assessment for each window
    # populates the steady_matrix with arrays of 0s and 1s that correspond to a window being unsteady or steady
    if print_diagnostics:
        print('Performing sliding window t-test through data set')
    for i in range(len(test_data) - window_size + 1):

        window_data = test_data[i:i + window_size]
        time_data = time[i:i + window_size] - min(time[i:i + window_size])

        if test_type == 't_test':
            steady_matrix[i, i:i+window_size] = stats.t_test(data_array=window_data,
                                                   time_array=time_data,
                                                   alpha=alpha/100,
                                                   value_to_return=value_to_return)
        
        elif test_type == 'adf':
            steady_matrix[i, i:i+window_size] = stats.adf_test(timeseries=window_data,
                                                                     significance_level=alpha)
            
        elif test_type == 'kpss':
            steady_matrix[i, i:i+window_size] = stats.kpss_test(timeseries=window_data,
                                                                     significance_level=alpha)

        # for example, for the array with elements 1 - 9, where the window size is 7, there are three windows
        # evaluated as the window size of 7

        # iterates over the 9 element long array.

        # 1 2 3 4 5 6 7 8 9 #

        # For example, the returned steady matrix might look like:
        # 1 1 1 1 1 1 1 X X #
        # X 0 0 0 0 0 0 0 X #
        # X X 1 1 1 1 1 1 1 #

        # Where X is an element outside the window at that particular iterative step

    # Saves the steady matrix (2d array of 0s and 1s if a visual check is needed of the steady test data matrix)
    if save_t_test_matrix:
        np.savetxt("steady_matrix_check.csv", steady_matrix)
    t_test_matrix = np.zeros(np.shape(steady_matrix)[1])

    # loops through the 2D steady matrix and averages the steady assessment values (0 or 1)
    # that are generated for each sample
    if print_diagnostics:
        print('Averaging t-test matrix results in time')
    for i in range(np.shape(steady_matrix)[1]):

        if (i - window_size) < 0:
            lower_limit = 0

        else:
            lower_limit = i + 1 - window_size

        upper_limit = i + 1

        t_test_matrix[i] = np.mean(steady_matrix[lower_limit:upper_limit, i])

        # the above for loop applied to the following steady matrix:
        # 0 0 1 1 1 1 0 X X #
        # X 1 1 1 1 0 0 0 X # 
        # X X 1 0 1 1 1 0 0 #

        # returns the following:
        # 0 0.5 1 0.66 1 0.66 0.33 0 0 #

    return t_test_matrix



def steady_state_start_end_region(time, t_test_data_array, pass_value=0.5, offset=20e-6, sampling_rate=4e-7):

    # finds the start and end point of the statistically determined steady test time based on the
    # user defined pass_value and offset (to account for flow start up phase that might be a false positive)

    offsetted = round(offset/sampling_rate)
    above_threshold = False
    start_index = None

    events = []

    for i, value in enumerate(t_test_data_array[offsetted:]):

        if not above_threshold and value > pass_value:

            # Data has risen above the threshold
            above_threshold = True
            start_index = i

        elif above_threshold and value < pass_value:

            # Data has now fallen below the fall threshold
            events.append((start_index+offsetted, offsetted+i))  # Store start and end index of the event
            above_threshold = False  # Reset for next even

    if not events:

        print("No steady test time found")
        return [0,0]

    else:
        return time[events][0][0], time[events][0][1]




