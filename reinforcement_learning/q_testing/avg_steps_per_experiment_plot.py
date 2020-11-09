import gym
import gym_chase
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser

from enviroment import q_training_from_experiment
from enviroment.q_tools import test_q_table

'''
Use several experiments to train a Q-Table, plot the amount of avg steps per experiment
'''
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--files', dest="filenames", nargs='+', help='<Required> Files to train the QTable',
                        required=True)
    args = parser.parse_args()

    experiments = args.filenames
    steps = []  # Amount of steps it takes to reach the goal in each testing iteration
    average_steps = []  # Amount of testing steps for each experiment
    q_table = None
    lower_error = []
    upper_error = []

    # Test with an empty Q Table so that the game plays randomly to compare amount of steps
    test_env = gym.make('chase-v0')
    test_env.set_num_row_cols(5)
    test_env.goal = (4, 4)
    q_table = np.zeros([test_env.observation_space, test_env.action_space])
    all_steps, avg_steps = test_q_table(env=test_env, q_table=q_table)
    steps.extend(all_steps)
    average_steps.append(avg_steps)
    lower_error.append(avg_steps - min(all_steps))
    upper_error.append(max(all_steps) - avg_steps)

    for experiment in experiments:

        # Train Q Table
        env = gym.make('chase-mental-v0')
        env.set_game_file(experiment)
        q_table = q_training_from_experiment.train_q_algorithm(gym_env=env, training_episodes=1, q_table=q_table)

        # Test Q Table
        test_env = gym.make('chase-v0')
        test_env.set_num_row_cols(5)
        test_env.goal = (4, 4)
        all_steps, avg_steps = test_q_table(env=test_env, q_table=q_table)
        steps.extend(all_steps)
        average_steps.append(avg_steps)
        lower_error.append(avg_steps - min(all_steps))
        upper_error.append(max(all_steps) - avg_steps)

    for step in steps:
        print(step)

    print("Averages")

    for avg_steps in average_steps:
        print(avg_steps)

    x = range(len(average_steps))
    y = average_steps
    plt.scatter(x=x, y=y)
    plt.xticks(np.arange(0, len(average_steps), 1))
    plt.errorbar(x, y, yerr=[lower_error, upper_error], fmt='o')
    plt.title("Average steps per experiment", fontsize=20)
    plt.xlabel("Experiments", fontsize=10)
    plt.ylabel("Average steps", fontsize=10)
    plt.show()
