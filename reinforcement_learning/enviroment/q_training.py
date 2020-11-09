import gym
import numpy as np
import random
import gym_chase
from argparse import ArgumentParser
from q_tools import write_q_table_file, test_q_table, read_q_table_file


def train_q_algorithm(gym_env, training_episodes, learning_rate=.8, y=.95, q_table=None):
    """
    Train Q table and return it
    :return: Q Table, average amount of steps when training
    """
    # Initialize Q-table with all zeros
    if q_table is None:
        q_table = np.zeros([gym_env.observation_space, gym_env.action_space])
    num_steps = 0
    steps_per_iteration = list()
    for i in range(training_episodes):
        # Reset environment and get first new observation
        state = gym_env.reset()
        # The Q-Table learning algorithm
        is_done = False
        print("training episode: ", i)
        while not is_done:
            new_state, reward, is_done, action = gym_env.step()
            # Update Q-Table with new knowledge

            q_table[state, action] = q_table[state, action] + learning_rate * (reward + y * np.max(q_table[new_state, :]) - q_table[state, action])
            state = new_state
        num_steps += gym_env.number_of_steps
        steps_per_iteration.append(gym_env.number_of_steps)
        test_env = gym.make('chase-v0')
        test_env.set_num_row_cols(5)
        test_env.goal = (4, 4)
        all_steps, avg_steps = test_q_table(env=test_env, q_table=q_table)
        print("All steps: ", all_steps, ", Avg steps: ", avg_steps)
    write_q_table_file(q_table)
    return q_table


if __name__ == "__main__":
    random.seed(12)
    parser = ArgumentParser()
    parser.add_argument("-q", "--quiet", dest="verbose", default=True, help="Don't print status messages to stdout")
    parser.add_argument('-f', '--files', dest="filenames", nargs='+', help='List of files that contain game information', required=True, type=str)
    parser.add_argument('-t', '--table', dest="qtable", help='File that contains Q Table', type=str)
    parser.add_argument('-c', '--classifier', dest="classifier", help='classifier', type=str)

    args = parser.parse_args()
    game_files = args.filenames

    if args.qtable is None:
        Q_table = None
    else:
        Q_table = read_q_table_file(args.qtable)

    env = gym.make('chase-mental-v0')
    for game_file in game_files:  # Use all the game files to train
        env.set_game_file(game_file)
        Q_table = train_q_algorithm(env, training_episodes=env.amount_of_experiences, q_table=Q_table)

