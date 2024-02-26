import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# TODO needs to be tidied up and properly tested

# Provided data
#  x_values = np.array([i for i in range(1, 207)])
#  y_values = np.array([1, 1, 2, 2, 3, 4, 3, 6, 8, 11, 9, 13, 11, 15, 10, 16, 14, 16, 20, 27, 24, 18, 27, 33, 32, 27, 42, 32, 33, 31, 46, 37, 31, 39, 45, 51, 44, 62, 48, 50, 45, 64, 54, 39, 50, 60, 68, 59, 81, 64, 66, 59, 82, 70, 48, 61, 74, 84, 73, 99, 80, 82, 73, 100, 86, 57, 72, 88, 100, 87, 117, 96, 98, 87, 118, 102, 66, 83, 102, 116, 101, 135, 112, 114, 101, 136, 118, 75, 94, 116, 132, 115, 153, 128, 130, 115, 154, 134, 84, 105, 130, 148, 129, 171, 144, 146, 129, 172, 150, 93, 116, 144, 164, 143, 189, 160, 162, 143, 190, 166, 102, 127, 158, 180, 157, 207, 176, 178, 157, 208, 182, 111, 138, 172, 196, 171, 225, 192, 194, 171, 226, 198, 120, 149, 186, 212, 185, 243, 208, 210, 185, 244, 214, 129, 160, 200, 228, 199, 261, 224, 226, 199, 262, 230, 138, 171, 214, 244, 213, 279, 240, 242, 213, 280, 246, 147, 182, 228, 260, 227, 297, 256, 258, 227, 298, 262, 156, 193, 242, 276, 241, 315, 272, 274, 241, 316, 278, 165, 204, 256, 292, 255, 333, 288, 290, 255, 334, 294, 174, 215, 270, 308, 269, 351, 304, 306, 269, 352, 310, 183, 226, 284, 324, 283, 369, 320, 322, 283, 370, 326, 192, 237, 298, 340, 297, 387, 336, 338, 297, 388, 342, 201, 248, 312, 356, 311, 405, 352, 354, 311, 406, 358, 210, 259, 326, 372, 325, 423, 368, 370, 325, 424, 374, 219, 270, 340, 388, 339, 441, 384, 386, 339, 442, 390, 228, 281, 354, 404, 353, 459, 400, 402, 353, 460, 406, 237, 292, 368, 420, 367, 477, 416, 418, 367, 478, 422, 246, 303, 382, 436, 381, 495, 432, 434, 381, 496, 438, 255, 314, 396, 452, 395, 513, 448, 450, 395, 514, 454, 264, 325, 410, 468, 409, 531, 464, 466, 409, 532, 470, 273, 336, 424, 484, 423, 549, 480, 482, 423, 550, 486, 282, 347, 438, 500, 437, 567, 496, 498, 437, 568, 502, 291, 358, 452, 516, 451, 585, 512, 514, 451, 586, 518, 300, 369, 466, 532, 465, 603, 528, 530, 465, 604, 534, 309, 380, 480, 548, 479, 621, 544, 546, 479, 622, 550, 318, 391, 494, 564, 493, 639, 560, 562, 493, 640, 566, 327, 402, 508, 580, 507, 657, 576, 578, 507, 658, 582, 336, 413, 522, 596, 521, 675, 592, 594, 521, 676, 598, 345, 424, 536, 612, 535, 693, 608, 610, 535, 694, 614, 354, 435, 550, 628, 549, 711, 624, 626, 549, 712, 630, 363, 446, 564, 644, 563, 729, 640, 642, 563, 730])

#  y_values = np.array([
#
#  1, 4, 9, 16, 24, 33, 43, 58, 69, 86, 101, 119, 142, 161, 189, 210, 244, 266, 304, 332,
#  373, 401, 439, 468, 512, 546, 598, 641, 692, 732, 797, 841, 910, 956, 1026, 1070, 1144,
#  1183, 1265, 1304, 1396, 1450, 1545, 1594, 1686, 1744, 1836, 1894, 1998, 2055, 2167, 2222,
#  2326, 2392, 2513, 2588, 2701, 2781, 2898, 2992, 3107, 3181, 3342, 3438, 3617, 3703, 3881,
#  3971, 4153, 4201, 4390, 4441, 4633, 4689, 4883, 4945, 5135, 5210, 5405, 5481, 5669, 5750,
#  5938, 6023, 6231, 6329, 6525, 6613, 6822, 6919, 7123, 7222, 7438, 7545, 7753, 7856, 8074,
#  8179, 8410, 8505, 8732, 8825, 9066, 9173, 9404, 9526, 9760, 9897, 10122, 10264, 10473,
#  10639, 10852, 11022, 11238, 11423, 11643, 11817, 12053, 12221, 12460, 12647, 12878, 13047,
#  13271, 13477, 13687, 13903, 14123, 14353, 14569, 14776, 14997, 15208, 15451, 15674, 15903,
#  16150, 16366, 16619, 16827, 17096, 17313, 17594, 17804, 18086, 18296, 18575, 18797, 19070,
#  19293, 19589, 19798, 20085, 20290, 20608, 20811, 21142, 21341, 21679, 21852, 22218, 22388,
#  22764, 22942, 23309, 23498, 23859, 24040, 24428, 24611, 25005, 25215, 25614, 25811, 26189,
#  26398, 26792, 26989, 27386, 27582, 27991, 28177, 28588, 28794, 29236, 29450, 29868, 30081,
#  30513, 30753, 31172, 31367, 31874, 32156, 32699, 32957, 33487, 33749, 34283, 34457, 34950,
#  35131, 35631, 35828, 36329
#  ])

#  print(len(x_values), len(y_values))
# Perform quadratic regression
#  coefficients = np.polyfit(x_values, y_values, 2)
#  coefficients = np.polynomial.polynomial.Polynomial.fit(x_values, y_values, 2)
#  quadratic_fit = np.poly1d(coefficients)

# Generate y values from the quadratic fit
#  y_fit = quadratic_fit(x_values)

#  print(quadratic_fit(26501365))

# Plot the original data and the fitted curve
#  plt.scatter(x_values, y_values, label='Original Data')
#
#  plt.plot(x_values, y_fit, label='Quadratic Fit', color='red')
#  plt.xlabel('x')
#  plt.ylabel('y')
#  plt.title('Quadratic Regression Fit')
#  plt.legend()
#  plt.show()


# Sample data
#  x = [1, 2, 3, 4, 5]
#
#  y = [2, 4, 1, 5, 2]

#  # Plot the data
#  plt.plot(x, y, label='Sample Data')

#  # Add a grid with lines every 1 unit on both axes
#  plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7, color='gray')

#  # Add labels and a legend (optional)
#  plt.xlabel('X-axis')
#  plt.ylabel('Y-axis')
#  plt.title('Sample Plot with Grid')
#  plt.legend()

#  # Show the plot
#  plt.show()

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
