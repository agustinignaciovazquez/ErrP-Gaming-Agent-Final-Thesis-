import mne
import numpy as np
import utils
import joblib
from mne.preprocessing import Xdawn
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn import svm
from sklearn.linear_model import LogisticRegression

EVENTS_IDS = {'Closer': 10001, 'Further': 10002}
EVENTS_TMIN = 0.0
EVENTS_TMAX = 2.0

n_filter = 3


def get_experiences_hit_no_hit(file, ):
    """
    :param file: file that will be used to generate epochs and its corresponding labels.
    :return: the epochs and its corresponding labels.
    :rtype: tuple(matrix, list)
    """

    montage = ['standard_1020']
    sig_mne = mne.io.read_raw_brainvision(file, montage, preload=True)
    sig_mne.pick_types(eeg=True, stim=True)  # only use eeg and stim channels

    # Do not set reference
    # https://martinos.org/mne/dev/auto_tutorials/plot_eeg_erp.html#setting-eeg-reference
    # If an empty list is specified, the data is assumed to already have a proper reference
    # and MNE will not attempt any re-referencing of the data
    sig_mne, _ = mne.set_eeg_reference(sig_mne, [])

    # Read annotations
    vmrk_file = file[:-4] + "vmrk"
    annot = mne.read_annotations(vmrk_file)
    sig_mne.set_annotations(annot)
    events, event_ids = mne.events_from_annotations(sig_mne)
    # print(events)
    # Bandpass filter by agus
    sig_mne.filter(l_freq=0.5, h_freq=10)
    # Notch filter
    sig_mne.notch_filter(np.arange(50, 100, 50), filter_length='auto', phase='zero')
    sig_mne, events = sig_mne.copy().resample(10, npad='auto', events=events)

    #Split experiencies of the same file
    events_split = []
    counter = 0
    for event in events:
        if (event[2] == 10003):
            events_split.append([])
            counter = counter + 1
        events_split[-1].append(event)

    #print(events_split)

    experiences = []
    for index in range(counter):
        try:
            epochs_no_hits = mne.Epochs(sig_mne, events_split[index], {'Further': 10002}, tmin=EVENTS_TMIN,
                                        tmax=EVENTS_TMAX, baseline=(EVENTS_TMIN, EVENTS_TMAX),
                                        picks=None, preload=True, reject=None, flat=None, proj=False, decim=1,
                                        reject_tmin=None, reject_tmax=None, detrend=None, on_missing='error',
                                        reject_by_annotation=True, metadata=None, verbose=None)

            epochs_hits = mne.Epochs(sig_mne, events_split[index], {'Closer': 10001}, tmin=EVENTS_TMIN, tmax=EVENTS_TMAX,
                                     baseline=(EVENTS_TMIN, EVENTS_TMAX),
                                     picks=None, preload=True, reject=None, flat=None, proj=False, decim=1,
                                     reject_tmin=None, reject_tmax=None, detrend=None, on_missing='error',
                                     reject_by_annotation=True, metadata=None, verbose=None)

            #epochs_not_hits_resampled = epochs_no_hits.copy().resample(10, npad='auto')
            #epochs_hits_resampled = epochs_hits.copy().resample(10, npad='auto')
            #evoked_no_hits = epochs_not_hits_resampled.average()
            #evoked_hits = epochs_hits_resampled.average()

            evoked_no_hits = epochs_no_hits.average()
            evoked_hits = epochs_hits.average()



            #Save in file values of sum(abs(hits - no hits)) per channel
            #utils.get_separability_values(file, evoked_hits, evoked_no_hits, index)

            #Plot graphs with hits and no hits curves averaged and resampled per channel
            #utils.plot_hits_and_no_hits(evoked_hits, evoked_no_hits)

        except:
            print("Error: " + file)



    return experiences

def get_experiences(file):
    """
    :param file: file that will be used to generate epochs and its corresponding labels.
    :return: the epochs and its corresponding labels.
    :rtype: tuple(matrix, list)
    """

    montage = ['standard_1020']
    sig_mne = mne.io.read_raw_brainvision(file, montage, preload=True)
    sig_mne.pick_types(eeg=True, stim=True)  # only use eeg and stim channels

    # Do not set reference
    # https://martinos.org/mne/dev/auto_tutorials/plot_eeg_erp.html#setting-eeg-reference
    # If an empty list is specified, the data is assumed to already have a proper reference
    # and MNE will not attempt any re-referencing of the data
    sig_mne, _ = mne.set_eeg_reference(sig_mne, [])
    #Read annotations
    vmrk_file = file[:-4] + "vmrk"
    annot = mne.read_annotations(vmrk_file)
    sig_mne.set_annotations(annot)
    events, event_ids = mne.events_from_annotations(sig_mne)
    print(event_ids)


    # Bandpass filter
    sig_mne.filter(l_freq=0.5, h_freq=10)

    # Notch filter
    # sig_mne.notch_filter(np.arange(50, 100, 50), filter_length='auto', phase='zero')
    #sig_mne, events = sig_mne.copy().resample(10, npad='auto', events=events)

    # Split experiencies of the same file
    events_split = []
    counter = 0
    for event in events:
        if (event[2] == 10003):
            events_split.append([])
            counter = counter + 1
        events_split[-1].append(event)

    experiences = []
    for index in range(counter):
        epochs = mne.Epochs(sig_mne, events_split[index], EVENTS_IDS, tmin=EVENTS_TMIN, tmax=EVENTS_TMAX, baseline=None,
                        picks=None, preload=True, reject=None, flat=None, proj=False, decim=1,
                        reject_tmin=None, reject_tmax=None, detrend=None, on_missing='error',
                        reject_by_annotation=True, metadata=None, verbose=None)
        experiences.append(epochs.copy().resample(10, npad='auto'))
    #print(experiences)
    return experiences

def train_classifier(experiences, classifier_path, n=1, scikit_classifier=LogisticRegression(penalty='l1', solver='liblinear',
                                       multi_class='auto')):
    """
    TODO: hacer bien
    :param experiences:
    :param experiences:
    :param classifier_path:
    :param scikit_classifier:
    :return:
    """
    epochs = mne.concatenate_epochs(experiences)
    print(epochs)
    epochs_labels_aux = epochs.events[:, -1]

    further_label = 10002
    closer_label = 10001
    epochs_labels = np.array([1 if x == further_label else 0 if x == closer_label else x for x in epochs_labels_aux])


    classifier = make_pipeline(
        Xdawn(n_components=n_filter), # comentar linea para no tener xdawn
        mne.decoding.Vectorizer(),  # Transform n-dimensional array into 2D array of n_samples by n_features.
        MinMaxScaler(),  # Transforms features by scaling each feature to a given range (0, 1).
        scikit_classifier  # linear model for classification
    )

    classifier_fit = classifier.fit(epochs, epochs_labels)
    joblib.dump(classifier_fit, classifier_path)
    return classifier_fit

def get_epochs_data_list_hit_no_hit(file_list):
    for file in file_list:
        get_experiences_hit_no_hit(file)

def get_epochs_data_list(file_list):
    experiences_list = list()
    for file in file_list:
        epochs = get_experiences(file)
        experiences_list.extend(epochs)
    print(experiences_list)
    return experiences_list


