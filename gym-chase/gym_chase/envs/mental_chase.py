import gym
from math import floor


POSITION = 0
GOAL = 1
REWARD = 2

END_OF_EXPERIENCE = "--\n"

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def get_action_map():
    action_map = dict()
    action_map[UP] = "Up"
    action_map[RIGHT] = "Right"
    action_map[DOWN] = "Down"
    action_map[LEFT] = "Left"
    return action_map


def check_experience_validity(experience):
    if len(experience[REWARD]) != len(experience[POSITION]):
        raise Exception("Input file was invalid, different amount of rewards and positions")
    if len(experience[REWARD]) != len(experience[GOAL]):
        raise Exception("Input file was invalid, different amount of goals and positions")


def read_rewards_file(filename):
    rewards = list()
    file = open(filename, "r")
    lines = file.readlines()
    for l in lines:
        rewards.append(int(l.replace("\n", "")))
    return rewards


class MentalChaseEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.reached_goal = False
        self.number_of_steps = 0
        self.rows, self.cols, self.experiences = None, None, None
        self.action_space = 4
        self.observation_space = None
        self.amount_of_experiences = None
        self.state = None
        self.initial_state = self.state
        self.previous_state = self.state
        self.goal = None
        self.reached_goal = False
        self.turn = 0
        self.already_reset = False

    def set_game_file(self, game_file):
        """
        Read a file containing the state and return amount of rows and cols and a list with information on each experience
        :param filename: File from where the game is read, complete path
        :return: amount of rows, amount of cols and a list of experiences where each experience is identified by three lists
        one containing all positions, another containing all goals and the last one containing all rewards, all three lists
        should have the same size, since at the same position all three should represent the state of the game at one given
        moment
        """
        file = open(game_file, "r")
        lines = file.readlines()
        [rows, cols] = lines[0].replace("\n", "").split("x")
        experiences = list()
        experience = (list(), list(), list())  # position, goal, reward
        for line in lines[1:]:
            if line != "\n":
                if '-' in line and line != END_OF_EXPERIENCE and not line.startswith("-"):
                    [current_position, goal_position] = line.replace("\n", "").split("-")
                    experience[POSITION].append(int(current_position))
                    experience[GOAL].append(int(goal_position))
                elif line == END_OF_EXPERIENCE:
                    check_experience_validity(experience)
                    experiences.append(experience)
                    experience = (list(), list(), list())
                else:
                    experience[REWARD].append(int(line.replace("\n", "")))
        file.close()
        self.rows, self.cols, self.experiences = int(rows), int(cols), experiences
        self.observation_space = self.rows * self.cols
        self.amount_of_experiences = len(self.experiences)
        self.state = self.experiences[0][POSITION][0]
        self.goal = self.experiences[0][GOAL][0]
        self.initial_state = self.state
        self.previous_state = self.state

    def get_row_col_from_state(self, state):
        """
        From state represented in a matrix it returns a number which represents the state
        :param state: Matrix which represents state
        :return: Numerical value of state
        """
        row = floor(state / self.cols)
        col = state - row * self.cols
        return row, col

    def calculate_reward(self):
        """
        Get reward by popping the list of experiences that was read from the file and that contains the rewards
        :return: integer representing reward
        """
        return self.experiences[0][REWARD].pop(0)

    def get_action(self):
        """
        Get number that represents the action that has taken place
        :return: an integer representing the action that was taken, where 0 represents up, 1 represents right,
        2 represents down and 3 represents left.
        """
        if self.state == self.previous_state + 1:  # Right
            return RIGHT
        elif self.state == self.previous_state - 1:  # Left
            return LEFT
        elif self.state < self.previous_state:  # Up
            return UP
        else:  # Down
            return DOWN

    def step(self):
        """
        Advance game to the next step, it does this by reading the game file and getting next position, reward and goal
        :return: new state, reward for this step, boolean indicating if the goal was reached and action that was
        executed
        """
        self.number_of_steps += 1
        self.previous_state = self.state
        if len(self.experiences[0][POSITION]) != 0:
            self.state = self.experiences[0][POSITION].pop(0)
            self.goal = self.experiences[0][GOAL].pop(0)
        if len(self.experiences[0][POSITION]) == 0 or self.goal == self.state:
            self.reached_goal = True  # TODO ver que siempre llegue al goal
        return self.state, self.calculate_reward(), self.reached_goal, self.get_action()

    def reset(self):
        """
        Reset environment by removing the current experience from the list of experiences, reset the number of steps,
        set the state back to the initial state, and set boolean indicating if the goal was reached back to false
        :return:
        """
        if self.already_reset:
            self.experiences.pop(0)
            self.initial_state = self.experiences[0][POSITION][0]
        self.number_of_steps = 0
        self.state = self.initial_state
        self.reached_goal = False
        self.already_reset = True
        return self.state

    def render(self):
        """
        Render game state, by printing the state in the console
        :return:
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if i * self.cols + j == self.state:
                    print("X", end='')
                else:
                    print("-", end='')
            print()

    def is_valid_action(self, action):
        """
        Checks if given the current state an action is valid
        :param action: Action for which it's checking it's validity
        :return: Boolean representing if it's boolean or not
        """
        if self.state < self.cols and action == UP:
            return False
        if self.state >= self.rows*self.cols - self.cols and action == DOWN:
            return False
        if self.state % (self.cols) == 0 and action == LEFT:
            return False
        if self.state % (self.cols) == self.cols - 1 and action == RIGHT:
            return False
        return True


