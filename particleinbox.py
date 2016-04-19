# ============================================================================
# Numerical and plotting libraries
import numpy as np
import pylab as pl
from matplotlib.widgets import Slider, Button
# =============================================================================
#
# Simulation Constants.  Be sure to include decimal points on appropriate
# variables so they become floats instead of integers.

# Constants for particle in a box potential
BOX_MAX_POTENTIAL_CONSTANT = 500000.0e0  # v_constant is the potential outside box
BOX_STARTING_POSITION = 0.0e0  # starting position of box
BOX_LENGTH_CONSTANT = 2.0e0  # length of the box
BOX_TOTAL_DIVISION_CONSTANT = 1000  # number of spatial points to divide the box length into
BOX_PSI_u0_CONSTANT = 0  # value of wave function for 0th division
BOX_PSI_u0_ddu_CONSTANT = 1  # value of derivative of wave function for 0th division
BOX_PSI_uL_CONSTANT = 0  # value of wave function for last division
BOX_PSI_uL_ddu_CONSTANT = -1  # value of derivative of wave function for last division
# Variables for particle in a box potential
# current_spatial_division; for short names it is referred to as 'u' in other related variable
# psi_u; wave function as a function of u; pronounce psi of u
# psi_u_ddu; derivative of psi_u w.r.t. u; pronounce d psi by du
# psi_u_d2du2; double derivative of psi_u w.r.t. u; pronounce d2psi by du2
# Often, the elements of an array are originally unknown, but its size is known.
# Hence, NumPy offers several functions to create arrays with initial placeholder content.
# These minimize the necessity of growing arrays, an expensive operation.
psi_u_array = np.zeros(BOX_TOTAL_DIVISION_CONSTANT+1)
energy_eigen_values = []
# variables shared across gui callbacks, hence made global
xaxis = np.arange(0.0, BOX_TOTAL_DIVISION_CONSTANT+1, 1)
plot = None
s_energy = None
axes = None
displayed_energy_eigen_index = 0
# =============================================================================


def get_potential_particle_in_box(position):
    "returns potential at a position for particle in a box"
    if (position < BOX_STARTING_POSITION or position > BOX_LENGTH_CONSTANT):
        return BOX_MAX_POTENTIAL_CONSTANT
    elif (position == BOX_STARTING_POSITION or position == BOX_LENGTH_CONSTANT):
        return BOX_MAX_POTENTIAL_CONSTANT/2
    else:
        return 0


def get_position(current_division):
    "return position for corresponding current_division"
    return current_division * get_dx()


def get_dx():
    return (BOX_LENGTH_CONSTANT/BOX_TOTAL_DIVISION_CONSTANT)


def print_summary():
    "prints all constants"
    print 'One-dimensional Schrodinger equation'
    print "Potential type: particle in a box"
    print "Wave function (psi) at 0: ", BOX_PSI_u0_CONSTANT
    print "Wave function at L", BOX_PSI_uL_CONSTANT
    print "Derivative of Wave function at 0: ", BOX_PSI_u0_ddu_CONSTANT
    print "Derivative of Wave function at L", BOX_PSI_uL_ddu_CONSTANT
    print 'Potential height: ', BOX_MAX_POTENTIAL_CONSTANT
    print "Box Length: ", BOX_LENGTH_CONSTANT
    print "Box starting coordinate", BOX_STARTING_POSITION
    print "total divisions to use while calculating", BOX_TOTAL_DIVISION_CONSTANT


def calculate_psi(assumed_energy):
    "calculate psi values at all spacial points for current energy and"
    "returns number of times xaxis is cut"
    global psi_u_array
    psi_u = BOX_PSI_u0_CONSTANT
    psi_u_ddu = BOX_PSI_u0_ddu_CONSTANT
    psi_u_d2du2 = 0
    xaxis_cut_number = 0
    # runs for one extra because we are storing the value in the beginning
    for current_spatial_division in range(0, BOX_TOTAL_DIVISION_CONSTANT+1):
        psi_u_array[current_spatial_division] = psi_u
        potential = get_potential_particle_in_box(get_position(current_spatial_division))
        psi_u_d2du2 = (potential - assumed_energy) * psi_u
        psi_u_ddu = psi_u_ddu + psi_u_d2du2 * get_dx()
        psi_u = psi_u + psi_u_ddu * get_dx()
        if (psi_u_array[current_spatial_division] * psi_u < 0):
            xaxis_cut_number += 1
    return xaxis_cut_number


def calculate_eigen_psi(lower_limit, upper_limit, interval_size):
    global energy_eigen_values
    if (lower_limit >= upper_limit or upper_limit-lower_limit <= interval_size):
        return False
    iteration_size = (upper_limit - lower_limit) / interval_size
    index = 0
    prev_xaxis_cuts = 0
    while index < iteration_size:
        assumed_energy = lower_limit + index * interval_size
        if calculate_psi(assumed_energy) > prev_xaxis_cuts:
            energy_eigen_values.append(round(assumed_energy, 4))
            prev_xaxis_cuts += 1
        index += 1
    print "eigen values", energy_eigen_values


def show_plot():
    global s_energy, plot, axes
    plot, = pl.plot(xaxis, psi_u_array, '-')
    pl.plot(xaxis, np.zeros(BOX_TOTAL_DIVISION_CONSTANT+1), '-')
    # reposition plot for adding space for sliders
    pl.subplots_adjust(bottom=0.25)
    # axis labels and title
    pl.xlabel('division ')
    pl.ylabel('Energy (unkown)')
    pl.title('Potential type: particle in a box')
    # marking in plot
    pl.grid(True)
    x_scale = BOX_TOTAL_DIVISION_CONSTANT / 10
    y_scale = abs(max(psi_u_array) - min(psi_u_array))/4
    pl.xticks(np.arange(min(xaxis), max(xaxis), x_scale))
    pl.yticks(np.arange(min(psi_u_array), max(psi_u_array), min(y_scale, 1)))
    axes = pl.gca()
    # show slider for E
    ax_energy = pl.axes([0.25, 0.1, 0.65, 0.03], axisbg='lightgoldenrodyellow')
    default_energy_value = 0.0e0
    s_energy = Slider(ax_energy, 'Energy', 0.0, 1000.0, valinit=default_energy_value)
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
    print_summary()
    calculate_psi(assumed_energy)
    plot.set_ydata(psi_u_array)
    x_scale = BOX_TOTAL_DIVISION_CONSTANT / 10
    axes.xaxis.set_ticks(np.arange(min(xaxis), max(xaxis), x_scale))
    y_scale = abs(max(psi_u_array) - min(psi_u_array))/4
    axes.yaxis.set_ticks(np.arange(min(psi_u_array), max(psi_u_array), min(y_scale, 1)))
    axes.relim()
    axes.autoscale_view(True, True, True)
    pl.draw()


def resetOnClick(event):
    global s_energy
    s_energy.set_val(energy_eigen_values[displayed_energy_eigen_index])
    print "reset clicked"


def prevOnClick(event):
    global displayed_energy_eigen_index
    if displayed_energy_eigen_index == 0:
        return  # as there is no prev
    displayed_energy_eigen_index = displayed_energy_eigen_index - 1
    s_energy.set_val(energy_eigen_values[displayed_energy_eigen_index])
    print "reset clicked"


def nextOnClick(event):
    global displayed_energy_eigen_index
    if displayed_energy_eigen_index == len(energy_eigen_values)-1:
        return  # as there is no next
    displayed_energy_eigen_index = displayed_energy_eigen_index + 1
    s_energy.set_val(energy_eigen_values[displayed_energy_eigen_index])
    print "reset clicked"


def main():
    global displayed_energy_eigen_index
    print_summary()
    energy_lower_limit = 0
    energy_upper_limit = 1000
    energy_interval = 0.1
    calculate_eigen_psi(energy_lower_limit, energy_upper_limit, energy_interval)
    if len(energy_eigen_values) != 0:
        calculate_psi(energy_eigen_values[displayed_energy_eigen_index])
        displayed_energy_eigen_index = 0
        show_plot()
        s_energy.set_val(energy_eigen_values[displayed_energy_eigen_index])
    print "Good bye!"

main()  # start main function
