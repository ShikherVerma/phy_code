# =============================================================================
#
#              Quantum Simulation using Finite Difference Method
#
#      The simulation is carried out by using the FD algorithm applied
#      to the Schroedinger equation.  The program is intended to act as
#      a demonstration of the FD algorithm and can be used as an educational
#      aid for quantum mechanics and numerical methods.  The simulation
#      parameters are defined in the code constants and can be freely
#      manipulated to see different behaviors.
#
#      The code has three built-in potential functions for demonstration.
#
#      1) Potential Well
#      2) Harmonic Oscillator
#      3) Delta function
#
#       Author:  Shikher Verma <root@shikherverma.com>
#       Date:  15/04/2016
# ============================================================================
# Numerical and plotting libraries
import numpy as np
import pylab as pl
from matplotlib.widgets import Slider, Button
# =============================================================================
#
# Simulation Constants.  Be sure to include decimal points on appropriate
# variables so they become floats instead of integers.
#
# Constants for particle in a box potential
BOX_MAX_POTENTIAL_CONSTANT = 5.0e0  # v_constant is the potential outside box
BOX_STARTING_POSITION = 0.0e0  # starting position of box
BOX_LENGTH_CONSTANT = 2.0e0  # length of the box
BOX_TOTAL_DIVISION_CONSTANT = 50  # number of spatial points to divide the box length into
BOX_PSI_u0_CONSTANT = 0  # value of wave function for 0th division
BOX_PSI_u0_ddu_CONSTANT = 1  # value of derivative of wave function for 0th division
BOX_PSI_uL_CONSTANT = 0  # value of wave function for last division
BOX_PSI_uL_ddu_CONSTANT = -1  # value of derivative of wave function for last division
# Variables for particle in a box potential
current_spatial_division = 0  # for short names it is referred to as 'u' in other related variable
psi_u = BOX_PSI_u0_CONSTANT  # wave function as a function of u; pronounce psi of u
psi_u_ddu = BOX_PSI_u0_ddu_CONSTANT  # derivative of psi_u w.r.t. u; pronounce d psi by du
psi_u_d2du2 = 0  # double derivative of psi_u w.r.t. u; pronounce d2psi by du2
assumed_energy = 0.0e0  # assumed energy which we will check for being exigent value
# Often, the elements of an array are originally unknown, but its size is known.
# Hence, NumPy offers several functions to create arrays with initial placeholder content.
# These minimize the necessity of growing arrays, an expensive operation.
psi_u_array = np.zeros(BOX_TOTAL_DIVISION_CONSTANT+1)
xaxis = np.arange(0.0, BOX_TOTAL_DIVISION_CONSTANT+1, 1)
plot = None
s_energy = None
axes = None
# =============================================================================


def get_potential_particle_in_box(position):
    "returns potential at a position for particle in a box"
    if (position < BOX_STARTING_POSITION or position > BOX_LENGTH_CONSTANT):
        return BOX_MAX_POTENTIAL_CONSTANT
    elif (position == BOX_STARTING_POSITION or position == BOX_LENGTH_CONSTANT):
        return BOX_MAX_POTENTIAL_CONSTANT/2
    else:
        return 0


def get_position(current_spatial_division):
    "return position for corresponding current_spatial_division"
    return current_spatial_division * get_dx()


def get_dx():
    return (BOX_LENGTH_CONSTANT/BOX_TOTAL_DIVISION_CONSTANT)


def is_potential_eigen():
    return True  # ########## REMOVE ME ##########
    if current_spatial_division == BOX_TOTAL_DIVISION_CONSTANT and psi_u == BOX_PSI_uL_CONSTANT:
        return True
    else:
        return False


def print_summary():
    print 'One-dimensional Schrodinger equation'
    print "Potential type: particle in a box"
    print 'Wave function energy (E) :   ', assumed_energy
    print "Wave function (psi) at 0: ", BOX_PSI_u0_CONSTANT
    print "Derivative of Wave function at 0: ", BOX_PSI_u0_ddu_CONSTANT
    print 'Potential height: ', BOX_MAX_POTENTIAL_CONSTANT
    print "Box Length: ", BOX_LENGTH_CONSTANT


def calculate_psi():
    global current_spatial_division, psi_u_array, psi_u_ddu, psi_u_ddu, psi_u
    psi_u = BOX_PSI_u0_CONSTANT
    psi_u_ddu = BOX_PSI_u0_ddu_CONSTANT
    psi_u_d2du2 = 0
    for current_spatial_division in range(0, BOX_TOTAL_DIVISION_CONSTANT+1):
        psi_u_array[current_spatial_division] = psi_u
        if current_spatial_division % 10 == 0:
            print "position:", current_spatial_division * get_dx(), "psi: ", psi_u
        potential = get_potential_particle_in_box(get_position(current_spatial_division))
        psi_u_d2du2 = (potential - assumed_energy) * psi_u
        psi_u_ddu = psi_u_ddu + psi_u_d2du2 * get_dx()
        psi_u = psi_u + psi_u_ddu * get_dx()


def show_plot():
    global s_energy, plot, axes
    if is_potential_eigen():
        plot, = pl.plot(xaxis, psi_u_array, '-x')
        pl.plot(xaxis, np.zeros(BOX_TOTAL_DIVISION_CONSTANT+1), '-')
        # reposition plot for adding space for sliders
        pl.subplots_adjust(bottom=0.25)
        # axis labels and title
        pl.xlabel('division ')
        pl.ylabel('Energy (unkown)')
        pl.title('Potential type: particle in a box')
        # marking in plot
        pl.grid(True)
        pl.xticks(np.arange(min(xaxis), max(xaxis), 5))
        pl.yticks(np.arange(min(psi_u_array), max(psi_u_array), 1))
        axes = pl.gca()
        # show slider for E
        ax_energy = pl.axes([0.25, 0.1, 0.65, 0.03], axisbg='lightgoldenrodyellow')
        default_energy_value = 0.0e0
        s_energy = Slider(ax_energy, 'Energy', 0.0, 100.0, valinit=default_energy_value)
        s_energy.on_changed(update)
        # show reset button
        resetax = pl.axes([0.8, 0.025, 0.1, 0.04])
        button = Button(resetax, 'Reset', color='lightgoldenrodyellow', hovercolor='0.975')
        button.on_clicked(reset)
        # show plot
        pl.show()


def update(val):
    global assumed_energy, plot
    print "old value", assumed_energy, "new value", s_energy.val
    assumed_energy = s_energy.val
    print_summary()
    calculate_psi()
    plot.set_ydata(psi_u_array)
    axes.xaxis.set_ticks(np.arange(min(xaxis), max(xaxis), 5))
    axes.yaxis.set_ticks(np.arange(min(psi_u_array), max(psi_u_array), 1))
    axes.relim()
    axes.autoscale_view(True, True, True)
    pl.draw()


def reset(event):
    global s_energy
    s_energy.reset()
    print "reset clicked"


def main():
    print_summary()
    calculate_psi()
    show_plot()
    print "Good bye!"

main()  # start main function
