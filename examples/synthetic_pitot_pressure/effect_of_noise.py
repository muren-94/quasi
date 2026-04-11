from pitot_pressure_curve_generator import pitot_pressure_curve_generator
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size':9})
fig,(ax1, ax2, ax3) = plt.subplots(nrows=3,ncols=1, sharex=True, figsize=(4,5), layout='constrained')
ax3.set_xlabel("Time (us)")
for mpr in [0.25, 0.5, 0.75, 1]:
    x,y=pitot_pressure_curve_generator(50,100,mpr, noise_value=0)
    ax1.plot(x,y, label="MPR="+str(mpr))
    x,y=pitot_pressure_curve_generator(50,100,mpr, noise_value=10)
    ax2.plot(x,y,label="MPR="+str(mpr))
    x,y=pitot_pressure_curve_generator(50,100,mpr, noise_value=30)
    ax3.plot(x,y,label="MPR="+str(mpr))
noise_values = [0, 10, 30]
ax1.legend()
for count, ax in enumerate([ax1, ax2, ax3]):
    #ax.set_title("Noise level = {0}".format(noise_values[count]))
    ax.annotate("Noise $\sigma$ = {0}".format(noise_values[count]), xy=(-8, 600))
    ax.set_xlim(-10,75)
    ax.set_ylim(0,700)
    ax.set_ylabel("Pitot Pressure (kPa)")
plt.savefig("synthetic_shot_noise_levels.eps")
plt.savefig("synthetic_shot_noise_levels.svg")
plt.show()