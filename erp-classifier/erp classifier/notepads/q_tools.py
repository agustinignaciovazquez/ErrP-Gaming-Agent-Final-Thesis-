import random
import math
import numpy as np


def write_q_table_file(q_table, q_file="Q_Table.txt"):
    """
    Write the q table in a file that will be used to play game
    :param q_table: Q table to be written in file, has to be a matrix
    :param q_file: File name to write in
    """
    file = open(q_file, "w+")
    rows = len(q_table)
    cols = len(q_table[0])
    file.write(str(rows) + "x" + str(cols) + "\n")
    for i in range(len(q_table)):
        file.write(str(i) + "-" + "24\n")  # TODO: deshardcodear el objetivo del juego
    file.write("UP\n")
    file.write("RIGHT\n")
    file.write("DOWN\n")
    file.write("LEFT\n")
    for row in q_table:
        for col in row:
            file.write(str(col) + "\n")
    file.close()


def read_q_table_file(q_file="Q_Table.txt"):
    """
    Read Q table from file and return a matrix containing the values
    :param q_file: File from where to read q table values, first line has the q table dimensions, followed by the
    possible states, then the actions, and then all the values ordered by rows from left to right
    :return: Q table, two-dimensional list
    """
    file = open(q_file, "r")
    lines = file.readlines()
    rows_str, cols_str = lines[0].split("x")
    rows = int(rows_str)
    cols = int(cols_str)
    q_value_list = lines[rows+cols+1:]
    q_table = [[0 for _ in range(cols)] for _ in range(rows)]
    list_index = 0
    for i in range(rows):
        for j in range(cols):
            q_table[i][j] = q_value_list[list_index]
            list_index += 1
    return np.asarray(q_table).astype(np.float)


def test_q_table(env, q_table, testing_episodes=200):
    """
    Test Q Table, print the average amount of steps
    :param env: Environment which will be tested
    :param q_table: Q table which will be used to do testing
    :param testing_episodes: Amount of episodes
    :return: List of amount of steps for each episode, avg amount of steps per episode
    """
    num_steps = 0
    all_steps = list()
    random.seed(12)
    for i in range(testing_episodes):
        state = env.reset()
        is_done = False
        iterations = 0
        while not is_done and iterations < 1000:
            sorted_actions = reversed(np.argsort(q_table[state, :]))
            # action = list(sorted_actions)[0]
            max_value = - math.inf
            max_values = list()
            valid_actions = list()
            for a in sorted_actions:  # Check that we are using a valid action
                if env.is_valid_action(a):
                    action_value = q_table[state, :][a]
                    valid_actions.append(a)
                    if action_value > max_value:
                        max_value = action_value
                        max_values = list()
                        max_values.append(a)
                    elif action_value == max_value:
                        max_values.append(a)
            rand = random.uniform(0, 1)
            if rand <= 0.05:
                action = random.choice(valid_actions)
            else:
                action = random.choice(max_values)
            state_new, reward, is_done, _ = env.step(action)
            state = state_new
            iterations += 1
            if is_done:
                num_steps += env.number_of_steps
                all_steps.append(env.number_of_steps)
                break
    average_steps = num_steps/testing_episodes
    return all_steps, average_steps
