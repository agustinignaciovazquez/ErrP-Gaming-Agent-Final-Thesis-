import trainer
import tester
import utils
import numpy as np

def grid_lights_rewards(prediction):
    if prediction == '4':
        return 10
    else:
        return prediction == '2' if -1 else 0

def get_hits_no_hits_file(file):
    stimulus = []

    with open(file, "r") as inp:

        for line in inp:
            if 'Stimulus' in line:

                dim = line.split(",")
                if dim[1][-1] != '3' and dim[1][-1] != '4':
                    stimulus.append(1 if dim[1][-1] == '2' else 0)
    return stimulus

hits_no_hits = get_hits_no_hits_file("../data/subject4/subject4-1/record-bv-generic-juan-[2019.05.25-15.25.17].vmrk")
array_hits_no_hits = np.asarray(hits_no_hits)

state_files = ["../data/subject4/subject4-1/grid_lights_experiment_juan_1",
               "../data/subject4/subject4-1/grid_lights_experiment_juan_2",
               "../data/subject4/subject4-1/grid_lights_experiment_juan_3"]

utils.merge_predictions_with_states(array_hits_no_hits, state_files, utils.grid_lights_rewards, "juan.txt")