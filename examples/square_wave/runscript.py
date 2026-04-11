from square_wave_generator import square_wave_generator
import quasi
from quasi.plotting import colorline
import numpy as np
import matplotlib.pyplot as plt

# Warning: AFD and KPSS tests do not run well with this test case

time_array, square_wave = square_wave_generator(plot=True)

t_test_matrix = quasi.core.sliding_window_test(
    time_data=time_array,
    test_data=square_wave,
    window_size=1,
    alpha=2.5,
    sampling_rate=np.max(time_array)/len(time_array),
    test_type='t_test')

fig, ax = plt.subplots(figsize=(6,4))
ax.set_title('Square Wave Steady Result')
lc = colorline(time_array, square_wave, t_test_matrix)
ax.set_xlim(xmin=np.min(time_array), xmax=np.max(time_array))
ax.set_ylim(ymin=-1.25, ymax=1.1*np.max(square_wave))
plt.colorbar(lc, label='Steady State (%)')
plt.tight_layout()

save = True
if save:
    plt.savefig('square_wave_output.png')
    plt.savefig('square_wave_output.svg')

plt.show()