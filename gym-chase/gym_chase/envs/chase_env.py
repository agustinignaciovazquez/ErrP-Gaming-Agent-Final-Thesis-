import random
import gym


def get_state_map(num_rows_cols):
    state_map = dict()
    state_number = 0
    for i in range(num_rows_cols):
        for j in range(num_rows_cols):
            base_matrix = [['-' for _ in range(num_rows_cols)] for _ in range(num_rows_cols)]
            base_matrix[i][j] = 'X'
            state_map[get_matrix_string(base_matrix)] = state_number
            state_number += 1
    return state_map


def get_action_map():
    action_map = dict()
    action_map[0] = "Up"
    action_map[1] = "Right"
    action_map[2] = "Down"
    action_map[3] = "Left"
    return action_map


def get_matrix_string(matrix):
    matrix_string = ""
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == "G":
                matrix_string += "-,"
            else:
                matrix_string += matrix[i][j] + ","
    return matrix_string


class ChaseEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, num_row_cols=5, initial_pos=(0, 0), goal=(4, 4), accuracy=1.0):
        self.reached_goal = False
        self.state = [['-' for _ in range(num_row_cols)] for _ in range(num_row_cols)]
        self.state[initial_pos[0]][initial_pos[1]] = "X"
        self.num_rows_cols = num_row_cols
        self.current_position = initial_pos
        self.prev_position = initial_pos
        self.goal = goal
        self.state[goal[0]][goal[1]] = "G"
        self.number_of_steps = 0
        self.initial_position = initial_pos
        self.state_map = get_state_map(num_row_cols)
        self.action_map = get_action_map()
        self.observation_space = len(self.state_map.keys())
        self.action_space = 4
        self.accuracy = accuracy

    def set_num_row_cols(self, row_cols):
        self.num_rows_cols = row_cols
        self.state_map = get_state_map(row_cols)

    def is_valid_action(self, action):
        if action == 0 and self.current_position[0] == 0:
            return False
        if action == 1 and self.current_position[1] == self.num_rows_cols - 1:
            return False
        if action == 2 and self.current_position[0] == self.num_rows_cols - 1:
            return False
        if action == 3 and self.current_position[1] == 0:
            return False
        if action < 0 or action > 3:
            return False
        return True

    def calculate_reward(self):
        reward = 0
        # Distance on x axis between goal and position increased
        if abs(self.current_position[0] - self.goal[0]) > abs(self.prev_position[0] - self.goal[0]):
            reward = -1
        # Distance on y axis between goal and position increased
        if abs(self.current_position[1] - self.goal[1]) > abs(self.prev_position[1] - self.goal[1]):
            reward = -1
        # Return correct reward with accuracy
        if random.uniform(0, 1) < self.accuracy:
            return reward
        else:
            return 0

    def step(self, action):
        """
        Iterate from one state to the next given an action
        :param action: Action that will change the state
        :return: state, reward, reachedGoal, numberOfSteps
        """
        self.number_of_steps += 1
        self.prev_position = self.current_position

        if not self.is_valid_action(action):
            print("Invalid action")
            if action < 0 or action > 3:
                print("Action out of bounds, action was " + str(action))
            else:
                print("Direction was towards " + self.action_map[action])
            return self.state_map[get_matrix_string(self.state)], 0, self.reached_goal, self.number_of_steps

        if action == 0:  # Upwards Direction
            self.state[self.current_position[0]][self.current_position[1]] = "-"
            self.state[self.current_position[0] - 1][self.current_position[1]] = "X"
            self.current_position = (self.current_position[0] - 1, self.current_position[1])

        elif action == 1:  # Right Direction
            self.state[self.current_position[0]][self.current_position[1]] = "-"
            self.state[self.current_position[0]][self.current_position[1] + 1] = "X"
            self.current_position = (self.current_position[0], self.current_position[1] + 1)

        elif action == 2:  # Downwards Direction
            self.state[self.current_position[0]][self.current_position[1]] = "-"
            self.state[self.current_position[0] + 1][self.current_position[1]] = "X"
            self.current_position = (self.current_position[0] + 1, self.current_position[1])

        elif action == 3:  # Left Direction
            self.state[self.current_position[0]][self.current_position[1]] = "-"
            self.state[self.current_position[0]][self.current_position[1] - 1] = "X"
            self.current_position = (self.current_position[0], self.current_position[1] - 1)

        else:
            print("Attempted action was " + str(action))
            raise Exception("Action is not valid since it is not in the action space")

        reward = self.calculate_reward()
        if self.current_position == self.goal:
            self.reached_goal = True
            reward = 10
        return self.state_map[get_matrix_string(self.state)], reward, self.reached_goal, self.number_of_steps

    def reset(self):
        self.number_of_steps = 0
        self.state = [['-' for _ in range(self.num_rows_cols)] for _ in range(self.num_rows_cols)]
        self.state[self.initial_position[0]][self.initial_position[1]] = "X"
        self.state[self.goal[0]][self.goal[1]] = "G"
        self.reached_goal = False
        self.current_position = self.initial_position
        return self.state_map[get_matrix_string(self.state)]

    def render(self, mode='human', close=False):
        for i in range(self.num_rows_cols):
            for j in range(self.num_rows_cols):
                print(self.state[i][j] + " ", end = '')
            print()

