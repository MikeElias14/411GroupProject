import matplotlib.pyplot as plt
import numpy as np


def main():

    # Given, meters
    h = 1
    x_in = 12
    y_in = 14
    unit_price = 895
    watts = 70661

    # Constraints
    min_z = 2
    max_z = h
    min_i = 300
    max_i = 500

    # Variables
    # position, in metres of each light
    num_lights = 0
    pos_x = []
    pos_y = []
    pos_z = 4

    # plotting
    path_x = []
    path_y = []

    # This funct is given point_x and point_y in cm
    def get_lux(point_x, point_y):
        i = 0
        for m in range(num_lights):
            i += watts / ((4 * np.pi) * (pos_z**2 + (point_x - pos_x[m])**2 + (point_y - pos_y[m])**2))
        return i

    def set_starting_points(n):
        pos_x = []
        pos_y = []
        path_x = []
        path_y = []

        p = (x_in+y_in)*2

        seg = p/n

        for i in range(n):
            dist = seg*i

            if dist <= x_in:
                pos_x.append(dist)
                pos_y.append(0)
            elif x_in < dist <= x_in+y_in:
                pos_x.append(x_in)
                pos_y.append(dist-x_in)
            elif x_in+y_in < dist <= (2*x_in)+y_in:
                pos_x.append(x_in-(dist-(x_in+y_in)))
                pos_y.append(y_in)
            elif (2*x_in)+y_in < dist:
                pos_x.append(0)
                pos_y.append(y_in-(dist-((2*x_in)+y_in)))

        print("Starting points x: " + str(pos_x))
        print("Starting points y: " + str(pos_y))

        return pos_x, pos_y

    def move_lights():
        mid_x = x_in/2
        mid_y = y_in/2
        for i in range(num_lights):
            x0 = pos_x[i]
            y0 = pos_y[i]
            if x0 - 0.1 <= mid_x <= x0 + 0.1 or y0 - 0.1 <= mid_y <= y0 + 0.1:
                print("add a light!")
                return False

            if x0 < mid_x:
                x = x0 + 0.01
                y = ((mid_y - y0) / (mid_x - x0)) * (x - x0) + y0
            else:  # x0 > mid_x:
                x = x0 - 0.01
                y = ((mid_y - y0) / (mid_x - x0)) * (x - x0) + y0
            #         print(x, mid_x, y, mid_y)

            pos_x[i] = round(x, 2)
            pos_y[i] = round(y, 2)
        #         print(pos_x, pos_y)
        return True

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
        for i in range(len(pos_x)):
            pos_x[i] *= 100
            pos_y[i] *= 100
        plt.scatter(pos_y, pos_x)
        plt.show()

    # Room is a 2d array of lxw, in cm, at reading level
    room = np.zeros(shape=(x_in*100, y_in*100))
    x_shape = room.shape[0]
    y_shape = room.shape[1]

    passed = False
    while not passed:
        num_lights += 1
        pos_x, pos_y = set_starting_points(num_lights)

        done = False
        while not done:
            for j in range(0, x_shape):
                for k in range(0, y_shape):
                    lux = get_lux(j/100, k/100)
                    room[j, k] = lux  # pass meters to get_lux
                    if lux < min_i:
                        if not move_lights():
                            done = True
                        passed = False
                        break
                else:
                    continue
                break
            else:
                passed = True
                done = True

    print("num_lights: " + str(num_lights))
    print("pos_x: " + str(pos_x))
    print("pos_y: " + str(pos_y))
    heatmap2d(room)


if __name__ == "__main__":
    main()
