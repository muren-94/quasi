import numpy as np
import matplotlib.pyplot as plt



def pitot_pressure_curve_generator(required_test_time_length=50, required_test_time_signal_value=100, mean_peak_ratio=1, time_increment=0.4, noise_value=10,
                      plot = False, save_to_csv = False):

    # Parameters for the normal distribution
    mu = 0         # mean
    sigma = 5 / (np.sqrt(2*np.pi))      # standard deviation
    x_range = np.arange(-10,10, time_increment)
    # Generate the normal distribution curve
    normal_dist = 2*(1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_range - mu) / sigma) ** 2)
    
    # Find the index where to transition to the sine wave (at half the normal distribution's tail)
    transition_point = np.where((normal_dist <=np.max(normal_dist)*mean_peak_ratio) & (x_range >= 0))[0][0]
    x_range_truncated = x_range[:transition_point]
    normal_dist_truncated = normal_dist[:transition_point]

    # Create the sine wave segment (10 wavelengths)
    sine_wave_unit_length = 6.283185307179586
    sine_wave_multiplier = required_test_time_length / sine_wave_unit_length
    sine_wave_length = sine_wave_multiplier*(2 * np.pi)
    sine_wave_x = np.arange(x_range_truncated[-1], x_range_truncated[-1] + sine_wave_length, time_increment)
    sine_wave_y = normal_dist_truncated[-1] + np.sin(sine_wave_x-np.min(sine_wave_x)+np.pi) / 200

    # After the sine wave, transition into a straight rising line
    straight_line_start = sine_wave_x[-1]
    straight_line_x = np.arange(straight_line_start, straight_line_start + 30, time_increment)

    rising_sin_curve = sine_wave_y[-1] + np.sin(straight_line_x-np.min(straight_line_x)+np.pi) /10 + (straight_line_x - np.min(straight_line_x)) / 50

    required_multiplier = required_test_time_signal_value / np.mean(sine_wave_y)
    total_x = np.concatenate((x_range[:transition_point], sine_wave_x, straight_line_x))
    total_y = np.concatenate((normal_dist[:transition_point], sine_wave_y, rising_sin_curve)) * required_multiplier

    total_x = np.linspace(total_x[0], total_x[-1], len(total_y))
    noise = np.random.normal(0, noise_value, len(total_y))
    total_y = total_y + noise

    if save_to_csv:
        np.savetxt("shot_simulation.csv", [total_x, total_y], delimiter=",")

    if plot:
        plt.figure(figsize=(6, 4))

        # Plot the normal distribution part
        plt.plot(x_range[:transition_point], normal_dist[:transition_point] * required_multiplier, label='Flow Arrival', color='b')

        # Plot the sine wave part
        plt.plot(sine_wave_x, sine_wave_y * required_multiplier, label='Steady Test Time', color='r')

        # Plot the straight line part
        plt.plot(straight_line_x, rising_sin_curve * required_multiplier, label='Unsteady Expansion Waves', color='g')

        # Labels and title
        # plt.title("Synthentic Pitot Pressure")
        plt.xlabel(r"Time (µs)")
        plt.ylabel("Pitot Pressure (kPa)")
        plt.legend()
        plt.xlim(np.min(total_x), np.max(total_x))
        plt.ylim(np.min(total_y), np.max(total_y))

        plt.tight_layout()

        plt.savefig('synthetic_pitot_pressure.svg')
        # Show the plot
        plt.close() 

    return total_x, total_y



if (__name__ == '__main__'):
    # Call the function to display the plot
    x,y = pitot_pressure_curve_generator(required_test_time_length=50, required_test_time_signal_value=100, mean_peak_ratio=0.25, noise_value=0)








