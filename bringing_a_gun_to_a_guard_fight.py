# I apologize for ever doubting MatLabs credibility as a programming language

from math import sqrt, atan2


def zeros_matrix(rows, cols):
    """
    Creates a matrix filled with zeros.
        :param rows: the number of rows the matrix should have
        :param cols: the number of columns the matrix should have

        :return: list of lists that form the matrix
    """
    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0)

    return M


def copy_matrix(M):
    """
    Creates and returns a copy of a matrix.
        :param M: The matrix to be copied

        :return: A copy of the given matrix
    """
    # Section 1: Get matrix dimensions
    rows = len(M)
    cols = len(M[0])

    # Section 2: Create a new matrix of zeros
    MC = zeros_matrix(rows, cols)

    # Section 3: Copy values of M into the copy
    for i in range(rows):
        for j in range(cols):
            MC[i][j] = M[i][j]

    return MC


def translate_y(matrix):
    """Translate the matrix around the right wall of the room"""
    og_matrix = copy_matrix(matrix)
    for i in range(len(matrix)):
        matrix[i].pop()

    for i in range(len(matrix)):
        for k in range(len(og_matrix[i])):
            matrix[i].append(og_matrix[i][-1 + -k])

    return matrix


def translate_x(matrix):
    """Translate the matrix around the bottom wall of the room"""
    og_matrix = copy_matrix(matrix)
    matrix.pop()
    for i in range(len(og_matrix) - 1, -1, -1):
        matrix.append(og_matrix[i])

    return matrix


def expand_matrix(matrix):
    """The 2 steps to expanding our original matrix"""
    copy_s1 = copy_matrix(matrix)
    step_1 = translate_y(copy_s1)
    copy_s2 = copy_matrix(step_1)
    step_2 = translate_x(copy_s2)
    return step_2


def get_max_matrix(matrix, max_row, max_col):
    """If matrix is smaller then firing range, the universe will expand"""
    while True:
        if len(matrix) >= max_row and len(matrix[0]) >= max_col:
            return matrix
        else:
            matrix = expand_matrix(matrix)


def filter_target_hit(matrix, player_col, player_row, max_distance):
    target = []
    for i in range(len(matrix)):
        dist = sqrt((matrix[i][1] - player_row) ** 2 + (matrix[i][0] -
        player_col) ** 2)
        angle = atan2(matrix[i][1] - player_row, matrix[i][0] - player_col)
        if max_distance > dist > 0:
            target.append([matrix[i], dist, angle])

    for m in range(len(target)):
        for n in range(len(target)):
            if target[m][2] == target[n][2] and target[m][1] > target[n][1]:
                target[m][0][2] = 0
    return target


def get_pos(matrix, pos, max_distance):
    """Gets all locations for player and guard + filters all possibilities
    that are out of firing range"""
    target = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            dist = sqrt((i - pos[0]) ** 2 + (j - pos[1]) ** 2)
            test_a = dist < max_distance
            test_b = matrix[i][j] == 7 or matrix[i][j] == 1
            if test_a and test_b:
                target.append([j, i, matrix[i][j]])
    return target


def other_quadrants(matrix, player_x_y, max_distance):
    q2 = copy_matrix(matrix)
    q2t = [-1, 1]
    q2f = []
    for j in range(len(q2)):
        list = [q2[j][i]*q2t[i] for i in range(2)]
        dist = sqrt((list[1] - player_x_y[1]) ** 2 + (list[0] -
                                                      player_x_y[0]) ** 2)
        if dist < max_distance:
            list.append(matrix[j][2])
            q2f.append(list)

    q3 = copy_matrix(matrix)
    q3t = [-1, -1]
    q3f = []
    for j in range(len(q3)):
        list = [q3[j][i]*q3t[i] for i in range(2)]
        dist = sqrt((list[1] - player_x_y[1]) ** 2 + (list[0] -
                                                      player_x_y[0]) ** 2)
        if dist < max_distance:
            list.append(matrix[j][2])
            q3f.append(list)

    q4 = copy_matrix(matrix)
    q4t = [1, -1]
    q4f = []
    for j in range(len(q3)):
        list = [q4[j][i]*q4t[i] for i in range(2)]
        dist = sqrt((list[1] - player_x_y[1]) ** 2 + (list[0] -
                                                      player_x_y[0]) ** 2)
        if dist < max_distance:
            list.append(matrix[j][2])
            q4f.append(list)

    return q2f, q3f, q4f


def trim(matrix, max_col, max_row):
    matrix = matrix[:max_row]

    for j in range(len(matrix)):
        matrix[j] = matrix[j][:max_col]

    return matrix


def return_count(matrix):
    count = 0
    for i in range(len(matrix)):
        if matrix[i][0][2] == 7:
            count += 1
    return count


def solution(dimensions, your_position, guard_position, distance):
    # Makes a matrix by using room dims

    matrix = [[0 for _ in xrange(dimensions[0] + 1)] for _ in xrange(
        dimensions[1] + 1)]

    # Places the player and the guard position in the room
    matrix[your_position[1]][your_position[0]] = 1
    matrix[guard_position[1]][guard_position[0]] = 7

    # Max possible rows and columns to a matrix, (your pos + distance)
    max_row = (your_position[1]) + distance + 1
    max_col = (your_position[0]) + distance + 1

    # Get a gird for the 1th quadrant.
    final_grid = get_max_matrix(matrix, max_row, max_col)
    final_grid = trim(final_grid, max_col, max_row)

    # Get all position in all quadrants
    first_q_pos = get_pos(final_grid, your_position, distance)
    q2, q3, q4 = other_quadrants(first_q_pos, your_position, distance)
    final_list = first_q_pos + q2 + q3 + q4

    # Filters the Original player, and all unattainable guards
    final_matrix = filter_target_hit(final_list, your_position[0],
                                     your_position[1], distance)
    count = return_count(final_matrix)
    return count





# dimensions = [23, 10]
# captain_position = [6, 4]
# badguy_position = [3, 2]
# distance = 23


dimensions = [10, 10]
captain_position = [4, 4]
badguy_position = [3, 3]
distance = 5000
# REAL answer = 739323



# dimensions = [2, 5]
# captain_position = [1, 2]
# badguy_position = [1, 4]
# distance = 11
# 0.0001 secs and result 27

# dimensions = [23, 10]
# captain_position = [6, 4]
# badguy_position = [3, 2]
# distance = 23
# 0.002 secs and result 8

# dimensions = [300, 275]
# captain_position = [150, 150]
# badguy_position = [180, 100]
# distance = 500
# 0.65 secs and result 9


# dimensions = [3, 2]
# captain_position = [1, 2]
# badguy_position = [2, 1]
# distance = 4
# 0 secs and result 7


# dimensions =1250, 1250],
# captain_position = [1000, 1000]
# badguy_position = [500, 400]
# distance = 10000
# 204 sec and result of 196

import time
start_time = time.time()
print solution(dimensions, captain_position, badguy_position, distance)
# print(solution([1250, 1250], [1000, 1000], [500, 400], 10000))
print("--- %s seconds ---" % (time.time() - start_time))


