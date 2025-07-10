import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# TODO needs to be tidied up and properly tested


def plot_2D(x, y):
    plt.plot(x, y, label='XY plot')
    plt.grid(True, which='both', linestyle='--',
             linewidth=0.5, alpha=0.7, color='gray')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('XY plot')
    plt.legend()
    plt.show()


def plot_3D(x, y, z):
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the points
    ax.scatter(x, y, z, c='b', marker='o')

    # Set labels and title
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.set_title('3D Scatter Plot')

    # Show plot
    plt.show()


class Animation:
    def __init__(self, frames_data):
        self.frames_data = frames_data

        # Create an empty scatter plot
        fig, ax = plt.subplots()
        self.scatter = ax.scatter([], [], c='green', marker='o')

        # Set plot limits
        ax.set_xlim(0, 200)
        ax.set_ylim(0, 200)

        # Create the animation
        self.animation = FuncAnimation(fig, self.update, frames=len(
            frames_data), interval=1000, blit=True)

        #  plt.grid(True)
        # Add a grid with lines every 1 unit on both axes
        #  plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7, color='gray')
        #
        plt.grid(which='major', color='gray', linewidth=1.2)
        plt.grid(which='minor', color='gray', linewidth=0.6)
        # Show the minor ticks and grid.
        plt.minorticks_on()
        # Now hide the minor ticks (but leave the gridlines).
        plt.tick_params(which='minor', bottom=False, left=False)

        # Locations for the X-axis, major grid
        #  ax.xaxis.set_major_locator(FixedLocator([1, 3, 5]))

        # Locations for the Y-axis, major grid
        #  ax.yaxis.set_major_locator(FixedLocator([1, 3, 5]))

        # Minor X and Y axis divided into n parts between each major grid
        ax.xaxis.set_minor_locator(AutoMinorLocator(25))
        ax.yaxis.set_minor_locator(AutoMinorLocator(25))

        # Only show minor gridlines once in between major gridlines.
        #  plt.xaxis.set_minor_locator(AutoMinorLocator(2))
        #  plt.yaxis.set_minor_locator(AutoMinorLocato

        # Show the plot
        plt.show()

    # Update function for animation
    def update(self, frame):
        # Get the points for the current frame
        points = self.frames_data[frame]

        # Update the x and y coordinates of the scatter plot
        self.scatter.set_offsets(points)
        return self.scatter,


def fit_polynomial(x_values, y_values):
    x_values = np.array(x_values)
    y_values = np.array(y_values)

    #  coefficients = np.polynomial.polynomial.Polynomial.fit(x_values, y_values, 2)
    #  return coefficients
    #  print(len(x_values), len(y_values))
    # Perform quadratic regression
    coefficients = np.polyfit(x_values, y_values, 2)
    #  coefficients = np.polynomial.polynomial.Polynomial.fit( x_values, y_values, 2)
    quadratic_fit = np.poly1d(coefficients)

    # Generate y values from the quadratic fit
    y_fit = quadratic_fit(x_values)

    print(quadratic_fit(26501365))

    # Plot the original data and the fitted curve
    plt.scatter(x_values, y_values, label='Original Data')
    plt.plot(x_values, y_fit, label='Quadratic Fit', color='green')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Quadratic Regression Fit')
    plt.legend()
    plt.show()
