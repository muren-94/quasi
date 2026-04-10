from scipy.signal import square
import matplotlib.pyplot as plt
import numpy as np



def square_wave_generator(number_of_points=1000, number_of_cycles=5, duty=0.25, plot=False):
    
    time_array = np.linspace(-np.pi/2, 2 * number_of_cycles * np.pi - np.pi/2, number_of_points)
    square_wave = square(t=time_array, duty=duty)

    if plot:
        fig, ax = plt.subplots()
        ax.plot(time_array, square_wave)
        plt.show()

    return time_array, square_wave



if (__name__ == '__main__'):
    time, square_wave = square_wave_generator(plot=True)



