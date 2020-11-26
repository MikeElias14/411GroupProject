import matplotlib.pyplot as plt
import numpy as np


def main():

    # Given, meters
    h = 1
    l = 3
    w = 3
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

    # This funct is given point_x and point_y in m
    def get_lux(point_x, point_y):
        i = 0
        for m in range(num_lights):
            i += watts / ((4 * np.pi) * (pos_z**2 + (point_x - pos_x[m])**2 + (point_y - pos_y[m])**2))
        return i

    def set_starting_points(n):
        pos_x = []
        pos_y = []
        p = (l+w)*2

        seg = p/n

        for i in range(n):
            dist = seg*i

            if dist <= l:
                pos_x.append(dist)
                pos_y.append(0)
            elif l < dist <= l+w:
                pos_x.append(l)
                pos_y.append(dist-l)
            elif l+w < dist <= (2*l)+w:
                pos_x.append(dist-(l+w))
                pos_y.append(w)
            elif (2*l)+w < dist:
                pos_x.append(0)
                pos_y.append(w-(dist-((2*l)-w)))

        return pos_x, pos_y

    def move_lights():
        mid_x = l*50
        mid_y = w*50
        for i in range(num_lights):
            x = pos_x[i]
            y = pos_y[i]

            if mid_x > x:
                pos_x[i] += 0.01
            elif mid_x < x:
                pos_x[i] -= 0.01

            if mid_y > y:
                pos_y[i] += 0.01
            elif mid_y < y:
                pos_x[i] -= 0.01
        return

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
    room = np.zeros(shape=(w*100, l*100))
    length = room.shape[0]
    width = room.shape[1]

    passed = False
    while not passed:
        num_lights += 1
        pos_x, pos_y = set_starting_points(num_lights)

        done = False
        while not done:
            for j in range(0, length):
                for k in range(0, width):
                    lux = get_lux(j/100, k/100)
                    room[j, k] += lux  # pass meters to get_lux
                    if lux < min_i:
                        move_lights()
                        passed = False
                        break
                else:
                    continue
                break
            else:
                passed = True
                done = True

    heatmap2d(room)

    print("num_lights: " + str(num_lights))
    print("pos_x: " + str(pos_x))
    print("pos_y: " + str(pos_y))


if __name__ == "__main__":
    main()
