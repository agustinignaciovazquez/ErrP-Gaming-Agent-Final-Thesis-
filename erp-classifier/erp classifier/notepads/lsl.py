from pylsl import StreamInlet, resolve_stream, StreamInfo
from threading import Thread
import tester
import mne
import numpy as np
import utils
import gym
import struct
import copy
import socket
import gym_chase
from q_tools import write_q_table_file, test_q_table, read_q_table_file
from math import floor
import random


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class ThreadTest():

    def eegStream(self, eeg_list):
        eeg = resolve_stream('type', 'EEG')
        eeg_inlet = StreamInlet(eeg[0])
        while True:
            sample, timestamp = eeg_inlet.pull_sample(timeout=0)
            print("EEG: " + str(timestamp))
            eeg_list.append((sample[:-1]))

    def markersStream(self, markers_list):
        markers = resolve_stream('type', 'Markers')
        marker_inlet = StreamInlet(markers[0])
        while True:
            marker_sample, marker_timestamp = marker_inlet.pull_sample(timeout=0)
            print("MARKER: " + str(marker_timestamp))
            markers_list.append(marker_sample)

    def positionStream(self, states_list, config_dict):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("localhost", 669)
        sock.bind(server_address)
        # Listen for incoming connections
        sock.listen(1)

        while True:
            # Wait for a connection
            connection, client_address = sock.accept()
            try:
                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(20)
                    if data:
                        arr_int = struct.unpack('!5I', data)
                        config_dict['dim'] = arr_int[0] * arr_int[1]
                        config_dict['games'] = arr_int[2]
                        config_dict['persued'] = arr_int[4]
                        states_list.append(str(arr_int[3]) + '-' + str(arr_int[4]))
                        #print("STATES:")
                        #print(states_list)
                    else:
                        print("No more data")
                        break

            finally:
                # Clean up the connection
                connection.close()

    def mainProgram(self, eeg_list, markers_list):
        markers_prev_size = 0
        eeg_prev_size = 0
        epoch_start = 0
        epoch_end = 0

        markers_pair = []
        while True:
            # if len(eeg_list) > eeg_prev_size:
            # for i in range(eeg_prev_size, len(eeg_list)):
            # print(eeg_list[i])
            #    eeg_prev_size = len(eeg_list)

            if len(markers_list) > markers_prev_size:
                for i in range(markers_prev_size, len(markers_list)):
                    markers_pair.append((markers_list[i][0], len(eeg_list)))
                    print((markers_list[i], len(eeg_list)))
                markers_prev_size = len(markers_list)

            if len(markers_pair) > 1 and (markers_pair[-2][0] == 1 or markers_pair[-2][0] == 2):
                epoch = eeg_list[markers_pair[-2][1]:markers_pair[-1][1]]
                # print(epoch)

    def predict_epoch(self, epoch, classifier):
        #signal = mne.io.RawArray(np.array(epoch).transpose(),
        #                         mne.create_info(['FZ', 'CZ', 'P3', 'PZ', 'P4', 'PO7', 'PO8', 'OZ'], sfreq=250,
        #                                         ch_types='eeg'))

        # signal.pick_types(eeg=True)
        #signal.filter(l_freq=0.5, h_freq=10, picks='eeg')
        # Notch filter
        #signal.notch_filter(np.arange(50, 100, 50), filter_length='auto', phase='zero')
        #epoch = mne.Epochs(signal, np.array([[0, 0, 1]]), {'Event': 1}, tmin=0.0,
        #                                tmax=2.0, baseline=(0.0, 2.0),
        #                                picks=None, preload=True, reject=None, flat=None, proj=False, decim=1,
        #                                reject_tmin=None, reject_tmax=None, detrend=None, on_missing='error',
        #                                reject_by_annotation=True, metadata=None, verbose=None)
        #epoch = epoch.copy().resample(10, npad='auto')
        #signal_aux = []
        #signal_aux.append(signal.get_data())
        #print(signal_aux)
        info = mne.create_info(['FZ', 'CZ', 'P3', 'PZ', 'P4', 'PO7', 'PO8', 'OZ'], sfreq=250, ch_types='eeg')
        events = np.array([[0, 0, 1]])
        epochs = np.array(epoch).transpose()
        epochs = np.array([epochs])
        epochArray = mne.EpochsArray(epochs, info=info, events=events, tmin=0, event_id={'arbitrary': 1})
        epochArray.filter(l_freq=0.5, h_freq=10)
        #epochArray.notch_filter(np.arange(50, 100, 50), filter_length='auto', phase='zero')
        epochArrayResampled = epochArray.copy().resample(10, npad='auto')
        prediction = classifier.predict(epochArrayResampled)
        return prediction

    def nonblocking_stream_reader(self, states, config_games):
        # wait to get the data
        while 'games' not in config_games:
            continue

        markers = []
        epochs = [[]]
        data_len = []
        data = []
        q_tables_array = []
        predictions = []
        counter = 0
        amount_of_games = config_games['games']
        dim = config_games['dim']

        #markers = resolve_stream('type', 'Markers')
        #marker_inlet = StreamInlet(markers[0])

        #eeg = resolve_stream('type', 'EEG')
        #eeg_inlet = StreamInlet(eeg[0])
        eeg_stream = resolve_stream('name', 'OpenViBE Stream')
        eeg_inlet = StreamInlet(eeg_stream[0])

        markers_stream = resolve_stream('name', 'openvibeMarkers')
        marker_inlet = StreamInlet(markers_stream[0])
        classifier = tester.get_classifier("classifiers.joblib")
        counter_samples = 0
        counter_marker = 0
        markers_hits_no_hits = []
        flag_save = False
        flag_new_epoch = False

        #dim = states.pop(0)  # First element is dimension
        q_table = np.zeros([dim, 4])
        prev_state = states.pop(0)

        test_env = gym.make('chase-v0')
        while amount_of_games > 0:
            marker_sample, marker_timestamp = marker_inlet.pull_sample(timeout=0)
            sample, timestamp = eeg_inlet.pull_sample(timeout=0)


            if sample is not None:
                data.append(sample)

            if marker_sample is not None and marker_sample[0] in [1, 2, 3, 4]:
                marker = marker_sample[0]
                markers.append(marker)
                print("MARKERS:")
                print(markers)
                data_len.append(len(data))
                #print(data_len)

                if marker == 1 or marker == 2 or marker == 4:
                    flag_save = True

                if marker == 3 and counter_samples == 500:
                    flag_save = False

            if len(markers) > 0 and markers[-1] == 3 and counter_samples == 500:
                flag_save = False

            if sample is not None:
                if flag_save:
                    if counter_samples < 500:
                        epochs[-1].append(sample[:-1])
                        counter_samples = counter_samples + 1
                    else:
                        counter_samples = 1
                        epochs.append([sample[:-1]])
                        flag_new_epoch = True
                        counter_marker = counter_marker + 1

            if flag_new_epoch:
                #print("LEN EPOCHS " + str(len(epochs)))
                prediction = self.predict_epoch(epochs[-2], classifier)
                predictions.append(prediction[0])
                print("PREDICTIONS:")
                print(predictions)
                aux_state = states.pop(0)
                is_done = self.train_q_table(prev_state, aux_state, prediction, q_table)
                if is_done:
                    amount_of_games = amount_of_games - 1
                    if amount_of_games > 0:
                        #dim = states.pop(0)
                        prev_state = states.pop(0)

                    q_tables_array.append(copy.deepcopy(q_table))


                else:
                    prev_state = aux_state
                flag_new_epoch = False

        for q_table_game in q_tables_array:
            counter = counter + 1
            test_env.set_num_row_cols(5)
            test_env.goal = (4, 4)
            all_steps, avg_steps = test_q_table(env=test_env, q_table=q_table_game, testing_episodes=200)
            print("All steps: ", all_steps, ", Avg steps: ", avg_steps)
            write_q_table_file(q_table_game, "QTable_" + str(counter) + ".txt")
        print(predictions)

    def train_q_table(self, prev_state, state, prediction, q_table):
        current_position, prev_position, reward, is_done, action = self.getStep(prev_state, prediction, state)
        # Update Q-Table with new knowledge
        learning_rate = .8
        y = .95
        q_table[prev_position, action] = q_table[prev_position, action] + learning_rate * \
                                         (reward + y * np.max(q_table[current_position, :]) - q_table[
                                             prev_position, action])
        return is_done

    def calculate_reward(self, reward):
        return utils.grid_lights_rewards(reward)

    def get_action(self, prev_pos, curr_pos):
        if curr_pos == prev_pos + 1:  # Right
            return RIGHT
        elif curr_pos == prev_pos - 1:  # Left
            return LEFT
        elif curr_pos < prev_pos:  # Up
            return UP
        else:  # Down
            return DOWN

    def getStep(self, prev_state, reward, state):
        [prev_position, prev_goal_position] = prev_state.split("-")
        [current_position, goal_position] = state.split("-")

        reward = None if (current_position == goal_position) else reward

        return int(current_position), int(prev_position), self.calculate_reward(reward), \
               (current_position == goal_position), self.get_action(int(prev_position), int(current_position))


if __name__ == '__main__':
    random.seed(12)
    state_files = ["../data/subject2/subject2-1/grid_lights_experiment_gonza_1",
                   "../data/subject2/subject2-1/grid_lights_experiment_gonza_2",
                   "../data/subject2/subject2-1/grid_lights_experiment_gonza_3"]
                   #"../../../data/subject1/subject1-1/grid_lights_experiment_alex_4"]
    states = utils.grid_lights_files_to_list(state_files)
    print(states)
    eeg_list = []
    markers_list = []
    #ThreadTest().nonblocking_stream_reader(states, len(state_files))
    states_list = []
    config_dict = dict()
    T1 = Thread(target=ThreadTest().positionStream, args=(states_list, config_dict))
    T2 = Thread(target=ThreadTest().nonblocking_stream_reader, args=(states_list, config_dict))
    T1.start()
    T2.start()
    T1.join()
    T2.join()

