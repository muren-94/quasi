from square_wave_generator import square_wave_generator
import steady_state_toolkit as sst
import numpy as np
import matplotlib.pyplot as plt

time_array, square_wave = square_wave_generator(plot=True)

t_test_matrix = sst.sliding_window.sliding_window_t_test(
    time_data=time_array,
    test_data=square_wave,
    window_size=1,
    sampling_rate=np.max(time_array)/len(time_array))

fig, ax = plt.subplots()
ax.set_title('Square Wave Steady Result')
lc = sst.plotting.colorline(time_array, square_wave, t_test_matrix)
ax.set_xlim(xmin=np.min(time_array), xmax=np.max(time_array))
ax.set_ylim(ymin=-1.25, ymax=1.1*np.max(square_wave))
plt.colorbar(lc, label='Steady State (%)')
plt.show()