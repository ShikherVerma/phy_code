# the function to be integrated
def func(x):
    return -0.25*x**2 + x + 4

# define variables
a = 1.          # left boundary of area
b = 5.          # right boundary of area
dx = 1          # width of the trapezoids

# calculate the number of trapezoids
n = int((b - a) / dx)

# define the variable for area
Area = 0

# loop to calculate the area of each trapezoid and sum.
for i in range(1, n+1):
    #the x locations of the left and right side of each trapezpoid
    x0 = a+(i-1)*dx
    x1 = a+i*dx

    #the area of each trapezoid
    Ai = dx * (func(x0) + func(x1))/ 2.

    # cumulatively sum the areas
    Area = Area + Ai

#print out the result.
print "Area = ", Area