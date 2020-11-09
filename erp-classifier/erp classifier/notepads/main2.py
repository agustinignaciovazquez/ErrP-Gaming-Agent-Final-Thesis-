import trainer
import tester
import utils

experiences_list = trainer.get_epochs_data_list(
    ['../data/grid_lights/nati/record-bv-generic-nati-[2019.04.27-19.11.05].vhdr'])

train_experiences = experiences_list[:3]
test_experiences = experiences_list[3:]

classifier = trainer.train_classifier(train_experiences, "../classifiers/nati.joblib")
classification = tester.test_classifier("../classifiers/nati.joblib", test_experiences)

state_files = ["/Users/franbartolome/Downloads/grid_lights_experiment_nati_4.txt",
               "/Users/franbartolome/Downloads/grid_lights_experiment_nati_5.txt"]

utils.merge_predictions_with_states(classification, state_files, utils.grid_lights_rewards, "../rewards/nati.txt")
