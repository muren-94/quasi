import steady_state_toolkit as sst
import numpy as np
import matplotlib.pyplot as plt
from steady_state_toolkit.plotting import colorline
from pitot_pressure_curve_generator import pitot_pressure_curve_generator

required_test_time_length = 100
required_test_time_signal_value = 50
window_size = 25
time_array, pitot_pressure = pitot_pressure_curve_generator(required_test_time_length=required_test_time_length, 
                                                            required_test_time_signal_value=required_test_time_signal_value, 
                                                            plot=False)

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(10,8))
fig.suptitle('Synthetic Pitot Pressure Steady Result')

axes = [ax1, ax2, ax3]

for ax, test_type in zip(axes, ['t_test', 'kpss', 'adf']):

    ax.set_title(test_type)

    t_test_matrix = sst.core.sliding_window_test(
        time_data=time_array,
        test_data=pitot_pressure,
        window_size=window_size,
        alpha=10,
        sampling_rate=np.max(time_array)/len(time_array),
        test_type=test_type)
    
    lc = colorline(time_array, pitot_pressure, t_test_matrix, axis=ax)
    ax.annotate(text='', xy=(0, 2*required_test_time_signal_value), xytext=(window_size, 2*required_test_time_signal_value), arrowprops=dict(arrowstyle='|-|'))
    ax.annotate(text='Sliding Window Length', xy=(10, 2.3*required_test_time_signal_value), xytext=(0, 2.3*required_test_time_signal_value))
    ax.set_xlim(xmin=np.min(time_array), xmax=np.max(time_array))
    ax.set_ylim(ymin=-1.25, ymax=1.1*np.max(pitot_pressure))
    ax.legend()
    fig.colorbar( lc, ax=ax, label='Steady State (%)')

fig.tight_layout()
plt.show()