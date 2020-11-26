import matplotlib.pyplot as plt
import numpy as np


def main():

    # Given, meters
    h = 1
    l = 1
    w = 1
    unit_price = 895
    watts = 70661

    # Constraints
    min_z = 2
    max_z = h
    intensity = 300

    # Variables
    num_lights = 1

    # position, in metres of each light
    pos_x = [0.25, 0.75]
    pos_y = [0.25, 0.75]
    pos_z = [4, 4]

    # This funct is given point_x and point_y in m
    def get_lux(point_x, point_y):
        i = 0
        for j in range(len(pos_x)):
            i += watts / ((4 * np.pi) * ((pos_z[j])**2 + (point_x - pos_x[j])**2 + (point_y - pos_y[j])**2))
        return i

    def get_hours():
        hours = 3 * (0.25 * h)
        return hours

    def get_labor_cost():
        time = get_hours()
        cost = time * (100 + (15 * (h - pos_z)))
        return cost

    def f():
        function = unit_price * num_lights + get_labor_cost()
        return function

    def heatmap2d(arr: np.ndarray):
        plt.imshow(arr, cmap='viridis')
        plt.colorbar()
        plt.show()

    # Room is a 2d array of lxw, in cm, at reading level
    room = np.arange(w*100 * l*100).reshape(h*100, l*100)
    length = room.shape[0]
    width = room.shape[1]

    for x in range(0, length):
        for y in range(0, width):
            room[x, y] = get_lux(x/100, y/100)  # pass meters to get_lux
    heatmap2d(room)


if __name__ == "__main__":
    main()