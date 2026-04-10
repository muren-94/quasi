from matplotlib.collections import LineCollection
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from .t_test import *
from .sliding_window import *
import os
import numpy as np



def colorline(x, y, z, contour_start_value=0, contour_end_value=100, linewidth=5, alpha=1.0, cmap='coolwarm_r', linestyle='-', axis=None):

    z = np.asarray(z) * 100

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, array=z, cmap=cmap,  linewidth=linewidth, alpha=alpha, linestyle=linestyle, norm=colors.BoundaryNorm(boundaries=np.linspace(contour_start_value,contour_end_value,11), ncolors=256))

    if axis is not None:
        axis.add_collection(lc)
    else:
        ax = plt.gca()
        ax.add_collection(lc)

    return lc



def assess_steady_state(dataset_name,
                        time_data,
                        test_data,
                        time_increment=4e-7,
                        window_size=50e-6,
                        alpha=0.025,
                        steady_time_identifier_offset=25e-6,
                        x_label=r"time ($\mu$s)",
                        y_label="pressure (kPa)",
                        pass_value=0.5,
                        plotting_style='individually',
                        show_plot=True,
                        find_start_and_end=False,
                        print_diagnostics=False,
                        value_to_return='steady_result'):
    # Function Description
    # this is a composite function that performs the steady test time assessment on a set of data
    # and plots the results on a signal magnitude vs time plot

    # creates an empty 2D matrix to store the t test results in
    ttest = np.zeros((len(time_data), len(test_data[0])))

    print('value to return: ', value_to_return)

    if plotting_style == 'individually':

        print('User has chosen to display signals on individual plots')

        plt.figure(figsize=(12, 8))
        plt.subplots_adjust(hspace=0.5)

        number_of_data_sets = len(test_data[0])
        nrows = ncols = int(np.ceil(np.sqrt(number_of_data_sets)))

        while nrows * ncols > number_of_data_sets:
            ncols = ncols - 1

        for count, value in enumerate(np.arange(1, number_of_data_sets + 1, 1)):

            print('-' * 60)
            print('Analysing signal number {0}'.format(count + 1))

            ax = plt.subplot(nrows, ncols, count + 1)

            ttest[:, count] = sliding_window_t_test(time_data, test_data[:, count], alpha, window_size, time_increment,
                                                    print_diagnostics=print_diagnostics, value_to_return=value_to_return)
            lc = colorline(time_data, test_data[:, count], ttest[:, count])
            plt.ylabel(y_label), plt.xlabel(x_label), plt.colorbar(lc, label='Steady State (%)')
            ax.set_xlim(time_data.min(), time_data.max()), ax.set_ylim(test_data[:].min(), test_data[:].max())

            if find_start_and_end:
                start = np.zeros(len(test_data[0]))
                end = np.zeros(len(test_data[0]))
                start[count], end[count] = steady_state_start_end_region(time_data, ttest[:, count], pass_value,
                                                                         steady_time_identifier_offset)
                plt.vlines(start[count], test_data[:].min(), test_data[:].max(), linestyles='--', color='black')
                plt.vlines(end[count], test_data[:].min(), test_data[:].max(), linestyles='--', color='black')
                ax.set_title(
                    "Signal" + str(value) + ", start time: " + str(round(start[count], 3)) + ", end time: " + str(
                        round(end[count], 3)) + ", test time: " + str(round(end[count] - start[count], 3)))
            else:
                ax.set_title("Signal" + str(value))

        plt.tight_layout()



    elif plotting_style == 'all':

        plt.rcParams.update({'font.size': 16})
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.subplots_adjust(hspace=0.5)

        # plt.suptitle("{0} {1} {2} trace".format(shot, model, data_type))
        for count, value in enumerate(np.arange(1, len(test_data[0]) + 1, 1)):
            print('-' * 60)
            print('Analysing signal number {0}'.format(count + 1))

            ttest[:, count] = sliding_window_t_test(time_data, test_data[:, count], alpha, window_size, time_increment,
                                                    print_diagnostics=print_diagnostics, value_to_return=value_to_return)
            lc = colorline(time_data, test_data[:, count], ttest[:, count])

        plt.ylabel(y_label), plt.xlabel(x_label), plt.colorbar(lc, label='Steady State (%)')
        ax.set_xlim(time_data.min(), time_data.max()), ax.set_ylim(test_data[:].min(), test_data[:].max())
        plt.tight_layout()



    elif plotting_style == 'pairs':

        plt.rcParams.update({'font.size': 16})
        fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
        axs = axs.flatten()

        # sets a subplot map so that the Pitot Pressure probes are plotted in pairs based on their radial
        # position from the core flow (PT1 & PT9, PT2 & PT8, etc)
        subplot_map = [0, 1, 2, 3, 3, 3, 2, 1, 0]

        for count, value in enumerate(np.arange(1, len(test_data[0]) + 1, 1)):
            print('-' * 60)
            print('Analysing signal number {0}'.format(count + 1))

            ax = axs[subplot_map[count]]
            ax.set_ylabel(y_label), ax.set_xlabel(x_label)
            ax.set_xlim(time_data.min(), time_data.max()), ax.set_ylim(test_data[:].min(), test_data[:].max())

            ttest[:, count] = sliding_window_t_test(time_data, test_data[:, count], alpha, window_size, time_increment,
                                                    print_diagnostics=print_diagnostics, value_to_return=value_to_return)
            lc = colorline(time_data, test_data[:, count], ttest[:, count], axis=ax)

        axs[0].annotate('PT1 and PT9', (100, 0.9 * test_data[:].max()))
        axs[1].annotate('PT2 and PT8', (100, 0.9 * test_data[:].max()))
        axs[2].annotate('PT3 and PT7', (100, 0.9 * test_data[:].max()))
        axs[3].annotate('PT4, PT5, PT6', (80, 0.9 * test_data[:].max()))

        plt.tight_layout(pad=2)
        plt.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.1, 0.03, 0.8])
        cb = fig.colorbar(lc, cax=cbar_ax)

    alpha_string = str(alpha)
    alpha_string = alpha_string.replace(".", "")

    if not os.path.exists("steady_test_time_output"):
        os.makedirs("steady_test_time_output")

    plt.savefig("steady_test_time_output/{0}_{1}_window_size_{2}_alpha".format(
        dataset_name, str(int(window_size)), alpha_string), bbox_inches='tight')

    plt.savefig("steady_test_time_output/{0}_{1}_window_size_{2}_alpha.eps".format(
        dataset_name, str(int(window_size)), alpha_string), bbox_inches='tight')

    plt.savefig("steady_test_time_output/{0}_{1}_window_size_{2}_alpha.svg".format(
        dataset_name, str(int(window_size)), alpha_string), bbox_inches='tight')

    if show_plot:
        plt.show()

    plt.close()

    return



def assess_steady_state_top_down(dataset_name,
                                 time_data,
                                 test_data,
                                 time_increment=4e-7,
                                 window_size=50e-6,
                                 alpha=0.025,
                                 x_label = "Signal Number",
                                 signal_names=[],
                                 show_plot=True,
                                 print_diagnostics=False):
    # Function Description
    # this is a composite function that performs the steady test time assessment on a set of pitot rake pressure
    # probe data and plots the results on a pressure vs time plot and a steadiness vs time plot

    # creates an empty 2D matrix to store the t test results in
    ttest = np.zeros((len(time_data), len(test_data[0])))

    for count, value in enumerate(np.arange(1, len(test_data[0]) + 1, 1)):
        print('-' * 60)
        print('Analysing signal number {0}'.format(count + 1))

        ttest[:, count] = sliding_window_t_test(time_data, test_data[:, count], alpha, window_size, time_increment,
                                                print_diagnostics=print_diagnostics)

    # creates empty arrays for start and end points for each pitot probe
    start = np.zeros(len(test_data[0]))
    end = np.zeros(len(test_data[0]))

    # "Top down" view of steadiness vs time that removes magnitude of pressure
    plt.figure(figsize=(10, 6))
    # plt.title("{0} {1} steady test time summary".format(shot, data_type)

    array = np.zeros((len(test_data[:, 0]), test_data.shape[1]))
    for i in range(test_data.shape[1]):
        array[:, i] = i + 1

    if not signal_names:
        signal_names = np.arange(1, test_data.shape[1] + 1, 1)

    for index, signal in enumerate(signal_names):
        lc = colorline(array[:, index], time_data[:], ttest[:, index], linewidth=10)
        plt.hlines(start[index], index + 1 * 0.8, index + 1 * 1.2, "k", linewidth=2)
        plt.hlines(end[index], index + 1 * 0.8, index + 1 * 1.2, "k", linewidth=2)

    print(np.shape(signal_names))
    plt.colorbar(lc, label='Steady State (%)'), plt.xlabel(x_label), plt.ylabel(r"time ($\mu$s)"), plt.grid()
    plt.xlim(0.5, len(signal_names)+0.5), plt.ylim(np.min(time_data), np.max(time_data))

    alpha_string = str(alpha)
    alpha_string = alpha_string.replace(".", "_")

    if not os.path.exists("steady_test_time_output"):
        os.makedirs("steady_test_time_output")

    plt.savefig("steady_test_time_output/{0}_{1}_window_size_{2}_alpha_summary".format(
        dataset_name, str(int(window_size)), alpha_string), bbox_inches='tight')

    plt.savefig("steady_test_time_output/{0}_{1}_window_size_{2}_alpha_summary.eps".format(
        dataset_name, str(int(window_size)), alpha_string), bbox_inches='tight')

    plt.savefig("steady_test_time_output/{0}_{1}_window_size_{2}_alpha_summary.svg".format(
        dataset_name, str(int(window_size)), alpha_string), bbox_inches='tight')

    if show_plot:
        plt.show()

    plt.close()

    return