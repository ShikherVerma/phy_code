# ============================================================================
# Numerical and plotting libraries
import numpy as np
import pylab as pl
from matplotlib.widgets import Slider, Button
# =============================================================================
#
# Simulation Constants. Be sure to include decimal points on appropriate
# variables so they become floats instead of integers.
negative_x_limit = -100  # number of divisions before 0
positive_x_limit = 100  # number of divisions after 0
total_x_length = 10.0  # total length on x axis to calculate for
# Note: for calculating the negative x limit in terms of length units multiply dx * negative_x_limit
dx = total_x_length / (abs(negative_x_limit) + abs(positive_x_limit))  # dx is total length by total divisions
xaxis = range(negative_x_limit, positive_x_limit + 1, 1)
# Variables for particle in a box potential
# Often, the elements of an array are originally unknown, but its size is known.
# Hence, NumPy offers several functions to create arrays with initial placeholder content.
# These minimize the necessity of growing arrays, an expensive operation.
psi_u_array = np.zeros(len(xaxis))
energy_eigen_values = []
plot = None
s_energy = None
axes = None
displayed_energy_eigen_index = 0
# =============================================================================


def get_symmertric_potential(position):
    "returns potential at a position"
    return abs(position) * 2


def get_position(current_division):
    "return position for corresponding current_division"
    return current_division * dx


def calculate_psi(assumed_energy, isEvenSolution):
    "calculate psi values at all spacial points for current energy"
    global psi_u_array, xaxis, dx
    if isEvenSolution:
        psi_u = 1
        psi_u_ddu = 0
    else:
        psi_u = 0
        psi_u_ddu = 1
    current_division = 0
    positive_xaxis = range(abs(negative_x_limit), len(xaxis), 1)
    for index in positive_xaxis:
        psi_u_array[index] = psi_u  # storing psi of current division
        if xaxis[index] != 0:
            if isEvenSolution:
                psi_u_array[len(xaxis) - index - 1] = psi_u
            else:
                psi_u_array[len(xaxis) - index - 1] = - psi_u
        current_division = xaxis[index]
        if (abs(psi_u) < 20):  # if psi is greater than 20 then it is most likely not going to diverge, so stop lengthy calculations
            potential = get_symmertric_potential(get_position(current_division))
            psi_u_d2du2 = (potential - assumed_energy) * psi_u  # psi by du2 at current division
            psi_u_ddu = psi_u_ddu + psi_u_d2du2 * dx  # psi by du at next division
            psi_u = psi_u + psi_u_ddu * dx  # psi at next division Using backward eular method


def calculate_eigen_psi(lower_limit, upper_limit, interval_size):
    global energy_eigen_values
    if (lower_limit >= upper_limit or upper_limit - lower_limit <= interval_size):
        return False
    iteration_size = (upper_limit - lower_limit) / interval_size
    index = 0
    isEvenSolution = True
    while index < iteration_size:
        assumed_energy = lower_limit + index * interval_size
        print assumed_energy, isEvenSolution
        calculate_psi(assumed_energy, isEvenSolution)
        if (round(psi_u_array[len(psi_u_array) - 1], 1) == 0):
            energy_eigen_values.append(assumed_energy)
            if isEvenSolution:
                isEvenSolution = False
            else:
                isEvenSolution = True
        index += 1
    print "eigen values", energy_eigen_values


def show_plot():
    global s_energy, plot, axes
    plot, = pl.plot(xaxis, psi_u_array, '-')
    pl.plot(xaxis, np.zeros(len(xaxis)), '-')
    potential = []
    for current_division in range(0, len(xaxis)):
        potential.append(get_symmertric_potential(get_position(xaxis[current_division])))
    pl.plot(xaxis, potential, '-')
    # reposition plot for adding space for sliders
    pl.subplots_adjust(bottom=0.25)
    # axis labels and title
    pl.xlabel('division ')
    pl.ylabel('Energy (unkown)')
    pl.title('Potential type: particle in a box')
    # marking in plot
    pl.grid(True)
    x_scale = len(xaxis) / 10
    y_scale = abs(max(psi_u_array) - min(psi_u_array)) / 4
    pl.xticks(np.arange(min(xaxis), max(xaxis), x_scale))
    pl.yticks(np.arange(min(psi_u_array), max(psi_u_array), min(y_scale, 1)))
    axes = pl.gca()
    # show slider for E
    ax_energy = pl.axes([0.25, 0.1, 0.65, 0.03], axisbg='lightgoldenrodyellow')
    default_energy_value = 0.0e0
    s_energy = Slider(ax_energy, 'Energy', 0.0, 10.0, valinit=default_energy_value)
    s_energy.on_changed(updateOnClick)
    # show reset button
    resetax = pl.axes([0.5, 0.025, 0.1, 0.04])
    reset_button = Button(resetax, 'Reset', color='lightgoldenrodyellow', hovercolor='0.975')
    reset_button.on_clicked(resetOnClick)
    # show prev button
    prevax = pl.axes([0.2, 0.025, 0.1, 0.04])
    prev_button = Button(prevax, 'Previous', color='lightgoldenrodyellow', hovercolor='0.975')
    prev_button.on_clicked(prevOnClick)
    # show next button
    nextax = pl.axes([0.8, 0.025, 0.1, 0.04])
    next_button = Button(nextax, 'Next', color='lightgoldenrodyellow', hovercolor='0.975')
    next_button.on_clicked(nextOnClick)
    # show plot
    pl.show()


def updateOnClick(val):
    global plot
    print "new value", s_energy.val
    assumed_energy = s_energy.val
    isEvenSolution = None
    index = 0
    while index < len(energy_eigen_values):
        if(assumed_energy <= energy_eigen_values[index]):
            print assumed_energy, energy_eigen_values[index], index
            if index % 2 == 0:
                isEvenSolution = True
            else:
                isEvenSolution = False
            break
        index += 1
    print assumed_energy, isEvenSolution
    calculate_psi(assumed_energy, isEvenSolution)
    plot.set_ydata(psi_u_array)
    x_scale = len(xaxis) / 10
    axes.xaxis.set_ticks(np.arange(min(xaxis), max(xaxis), x_scale))
    y_scale = abs(max(psi_u_array) - min(psi_u_array)) / 4
    axes.yaxis.set_ticks(np.arange(min(psi_u_array), max(psi_u_array), min(y_scale, 1)))
    axes.relim()
    axes.autoscale_view(True, True, True)
    pl.draw()


def resetOnClick(event):
    global s_energy
    s_energy.set_val(energy_eigen_values[displayed_energy_eigen_index])


def prevOnClick(event):
    global displayed_energy_eigen_index
    if displayed_energy_eigen_index == 0:
        return  # as there is no prev
    displayed_energy_eigen_index = displayed_energy_eigen_index - 1
    s_energy.set_val(energy_eigen_values[displayed_energy_eigen_index])


def nextOnClick(event):
    global displayed_energy_eigen_index
    if displayed_energy_eigen_index == len(energy_eigen_values) - 1:
        return  # as there is no next
    displayed_energy_eigen_index = displayed_energy_eigen_index + 1
    s_energy.set_val(energy_eigen_values[displayed_energy_eigen_index])


def main():
    global displayed_energy_eigen_index
    energy_lower_limit = 0
    energy_upper_limit = 10
    energy_interval = 0.00001
    calculate_eigen_psi(energy_lower_limit, energy_upper_limit, energy_interval)
    if len(energy_eigen_values) != 0:
        calculate_psi(energy_eigen_values[0], True)
        displayed_energy_eigen_index = 0
        show_plot()
        s_energy.set_val(energy_eigen_values[displayed_energy_eigen_index])
    print "Good bye!"

main()  # start main function
