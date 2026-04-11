import steady_state_toolkit as sst
import numpy as np
import matplotlib.pyplot as plt
from steady_state_toolkit.plotmethods import colorline
from pitot_pressure_curve_generator import pitot_pressure_curve_generator

required_test_time_length = 100
required_test_time_signal_value = 50
window_size = 25
time_array, pitot_pressure = pitot_pressure_curve_generator(required_test_time_length=required_test_time_length, 
                                                            required_test_time_signal_value=required_test_time_signal_value, 
                                                            plot=True)

t_test_matrix = sst.sliding_window.sliding_window_test(
    time_data=time_array,
    test_data=pitot_pressure,
    window_size=window_size,
    alpha=5,
    sampling_rate=np.max(time_array)/len(time_array),
    test_type='t_test')

fig, ax = plt.subplots()
ax.set_title('Synthetic Pitot Pressure Steady Result')

lc = colorline(time_array, pitot_pressure, t_test_matrix)
ax.annotate(text='', xy=(0, 2*required_test_time_signal_value), xytext=(window_size, 2*required_test_time_signal_value), arrowprops=dict(arrowstyle='|-|'))
ax.annotate(text='Sliding Window Length', xy=(0, 2.2*required_test_time_signal_value), xytext=(0, 2.2*required_test_time_signal_value))
ax.set_xlim(xmin=np.min(time_array), xmax=np.max(time_array))
ax.set_ylim(ymin=-1.25, ymax=1.1*np.max(pitot_pressure))
ax.legend()
plt.colorbar(lc, label='Steady State (%)')
plt.show()