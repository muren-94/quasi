import quasi
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

# Raw data import #
data = np.loadtxt('pressure_data.csv', delimiter=',', skiprows=1)
time = data[:,0]
pressures = data[:,1:]

# Plot the raw data
fig, ax = plt.subplots()
ax.set_title('Raw data')

for col in range(len(pressures[0,:])):

    #zero the data to account for offsets
    pressures[:,col] = scipy.signal.savgol_filter(pressures[:,col] - pressures[0,col], window_length=100, polyorder=2)

    ax.plot(time, pressures[:,col]-pressures[0,col], label=f"pt{col+1}")
    
ax.set_xlim(xmin=np.min(time), xmax=np.max(time))
ax.set_ylim(ymin=0, ymax=1.1*np.max(pressures))
ax.set_xlabel('Time')
ax.set_ylabel('Pressure')
ax.legend(loc='upper center', ncol=4)
plt.show()


# Now apply the sliding window methodology using the two-tailed t-test

fig, ax = plt.subplots()
for col in range(len(pressures[0,:])):

    print('Analysing signal#: ', col+1)

    t_test_matrix = quasi.core.sliding_window_test(
        time_data=time,
        test_data=pressures[:,col],
        window_size=20E-6,
        alpha=1,
        sampling_rate=4E-7,
        test_type='t_test')

    # Plotting the steadyness result of the averaged t-test matrix using the colorline function
    lc = quasi.plotting.colorline(time, pressures[:,col], t_test_matrix)

ax.set_xlim(xmin=np.min(time), xmax=np.max(time))
ax.set_ylim(ymin=0, ymax=1.1*np.max(pressures))
plt.colorbar(lc, label='Steady State (%)')
plt.tight_layout()
plt.show()
