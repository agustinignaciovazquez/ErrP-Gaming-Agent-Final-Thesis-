# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Information
#
# - Full paper: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4374466/

# # Libraries
#
# 1) Install Anaconda
#
#     - Run 'brew cask install anaconda'
#     - Add 'export PATH=/usr/local/anaconda3/bin:"$PATH"' to '.bash_profile' or to '.bashrc'
#
# 2) Install MNE (https://martinos.org/mne/stable/install_mne_python.html)
#
#     - Run 'conda --version && python --version'
#     - Run:
#         - curl -O https://raw.githubusercontent.com/mne-tools/mne-python/master/environment.yml
#         - conda env create -f environment.yml
#         - source activate mne

# ## Load libraries

# +
import matplotlib.pyplot as plt
import mne
import numpy as np

from random import randint
from scipy import interp
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
# -

# ## Config libraries

mne.set_log_level('WARNING')

# # Dataset

# ## Load signals
#
# - https://martinos.org/mne/stable/auto_tutorials/plot_creating_data_structures.html

# +
vhdr_file = './record-bv-[2019.04.06-13.19.45].vhdr'

# Set missing EEG montage (electrode positions)
# https://martinos.org/mne/stable/generated/mne.io.Raw.html#mne.io.Raw.set_montage
# https://mne-tools.github.io/stable/generated/mne.channels.Montage.html
# Electrodes are named and positioned according to the international 10-20 system (94+3 locations)
# https://en.wikipedia.org/wiki/10–20_system_(EEG)
montage = 'standard_1020'

sig_mne = mne.io.read_raw_brainvision(vhdr_file, montage, preload=True)

sig_mne.pick_types(eeg=True, stim=True)  # only use eeg and stim channels

# Do not set reference
# https://martinos.org/mne/dev/auto_tutorials/plot_eeg_erp.html#setting-eeg-reference
# If an empty list is specified, the data is assumed to already have a proper reference
# and MNE will not attempt any re-referencing of the data
sig_mne, _ = mne.set_eeg_reference(sig_mne, [])
sample_rate = sig_mne.info['sfreq']

print('Loaded subject from: {}'.format(vhdr_file))
print('Sample rate: {}'.format(sample_rate))
print(sig_mne)
# -

# ## Sensors

# Plot sensors
sig_mne.plot_sensors()
sig_mne.plot_sensors('3d')  # in 3D
sig_mne.plot_sensors('select')

# ## Plot signals

# Plot raw data of first 8 channels
sig_mne.plot(n_channels=8, scalings='auto', block=True)

# Compute the power spectral density of raw data
# https://martinos.org/mne/stable/auto_examples/time_frequency/plot_compute_raw_data_spectrum.html
sig_mne.plot_psd()

# +
# Band-pass filter data
sig_mne.filter(l_freq=1.0, h_freq=20.0)

# Plot the power spectral density across filtered channels
sig_mne.plot_psd()

# +
# start, stop = raw.time_as_index([100, 115])  # 100 s to 115 s data segment
# data, times = raw[:, start:stop]
# print(data.shape)
# print(times.shape)
# data, times = raw[2:20:3, start:stop]  # access underlying data
# raw.plot()
# -

# # Analisys

# ## Load events
#
# - https://martinos.org/mne/stable/auto_tutorials/plot_creating_data_structures.html
# - https://martinos.org/mne/stable/auto_examples/io/plot_read_events.html#ex-read-events

stim_channel_name = 'STI 014'
# Find events
# https://martinos.org/mne/stable/generated/mne.find_events.html
events = mne.find_events(sig_mne, stim_channel=stim_channel_name, output='step', consecutive=True,
                         min_duration=0, shortest_event=1, mask=None, uint_cast=False, mask_type='and',
                         initial_event=True, verbose=None)
print('Number of events:', len(events))
print('Event codes:', np.unique(events[:, 2]))  # Show all unique event codes (3rd column)

events_ids = {'Closer': 1, 'Further': 2}

# ## Plot events
#
# - https://martinos.org/mne/stable/auto_tutorials/plot_visualize_epochs.html

# Plot all events
mne.viz.plot_events(events, sfreq=sample_rate)  # https://martinos.org/mne/stable/generated/mne.viz.plot_events.html

# Plot Closer and Further events
mne.viz.plot_events(events, event_id=events_ids, sfreq=sample_rate)

# ## Load epochs

events_tmin = -0.2
events_tmax = 2.0
# Find epochs
# https://martinos.org/mne/stable/auto_tutorials/plot_object_epochs.html
epochs = mne.Epochs(sig_mne, events, events_ids, tmin=events_tmin, tmax=events_tmax, baseline=(None, 0),
                    picks=None, preload=True, reject=None, flat=None, proj=False, decim=1,
                    reject_tmin=None, reject_tmax=None, detrend=None, on_missing='error',
                    reject_by_annotation=True, metadata=None, verbose=None)
epochs_labels = epochs.events[:, -1]
print("Labels: ")
print(epochs_labels)
print(epochs)
print('Loaded (#Epochs, #Channels, #Times) = {}'.format(epochs.get_data().shape))

# ## Plot epochs
#
# https://martinos.org/mne/stable/auto_tutorials/plot_visualize_epochs.html

epochs.plot(scalings='auto', block=True)

# Plot average for each event type
for each in events_ids:
    epochs[each].average().plot(titles=('Event ' + each), time_unit='s', spatial_colors=True)

# Plot average for all types
epochs.average().plot(titles='All events', time_unit='s', spatial_colors=True)

# ## Train
#
# - http://scikit-learn.org/stable/tutorial/machine_learning_map/index.html
# - http://scikit-learn.org/stable/tutorial/basic/tutorial.html

target_names = ['noerror', 'error']
error_label = 2
hits_epochs_labels = np.array([1 if x == error_label else 0 for x in epochs_labels])
# random labels
# hits_epochs_labels = np.asarray([randint(0,1) for i in range(len(hits_epochs_labels))])
print(epochs_labels)
print(hits_epochs_labels)

# +
# Set classification pipeline
# TODO: Test classificators
classifier = make_pipeline(
    mne.decoding.Vectorizer(),  # Transform n-dimensional array into 2D array of n_samples by n_features.
    MinMaxScaler(),  # Transforms features by scaling each feature to a given range (0, 1).
    LogisticRegression(penalty='l2')  # linear model for classification
)

# Set cross-validator
# Stratified K-Folds cross-validator
# Provides train/test indices to split data in train/test sets
# This cross-validation object is a variation of KFold that returns stratified folds
# Stratification is done based on the labels provided in split(_, labels)
# The folds are made by preserving the percentage of samples for each class
# https://machinelearningmastery.com/k-fold-cross-validation/
# http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html
cross_validator = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# +
tprs = []
aucs = []
mean_fpr = np.linspace(0, 1, 100)
i = 0

plt.figure(figsize=(20, 10))

# Do cross-validation
for train_index, test_index in cross_validator.split(epochs, hits_epochs_labels):
    data_train, data_test = epochs[train_index], epochs[test_index]
    labels_train, labels_test = hits_epochs_labels[train_index], hits_epochs_labels[test_index]
    classification_fit = classifier.fit(data_train, labels_train)
    # classification_fit.predict(data_test)
    prediction_proba = classification_fit.predict_proba(data_test)

    # ROC curve for fold i
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html
    fpr, tpr, thresholds = roc_curve(labels_test, prediction_proba[:, 1])
    tprs.append(interp(mean_fpr, fpr, tpr))
    tprs[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs.append(roc_auc)
    plt.plot(fpr, tpr, lw=1, alpha=0.3, label='ROC fold %d (AUC = %0.2f)' % (i, roc_auc))
    i += 1

# Chance line
plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Chance', alpha=.8)
# Mean ROC
mean_tpr = np.mean(tprs, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs)
plt.plot(mean_fpr, mean_tpr, color='b', label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)
# Std. dev. ROC
std_tpr = np.std(tprs, axis=0)
tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2, label=r'$\pm$ 1 std. dev.')
# Plot ROC
plt.title('ROC curve')
plt.xlabel('False positive rate')
plt.xlim([-0.05, 1.05])
plt.ylabel('True positive radte')
plt.ylim([-0.05, 1.05])
plt.legend(loc="best")
plt.show()
# -

# https://scikit-learn.org/stable/modules/cross_validation.html
scoring = None
# scoring = 'roc_auc'
scores = cross_val_score(classifier, epochs.get_data(), hits_epochs_labels, cv=cross_validator, scoring=scoring)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

# +
predictions = cross_val_predict(classifier, epochs.get_data(), hits_epochs_labels, cv=cross_validator)
confusion_m = confusion_matrix(hits_epochs_labels, predictions)
print("Confusion matrix")
print(confusion_m)

# Normalized confusion matrix
confusion_m_norm = confusion_m.astype(float) / confusion_m.sum(axis=1)[:, np.newaxis]

# Plot it
plt.imshow(confusion_m_norm, interpolation='nearest', cmap=plt.cm.Blues)
tick_marks = np.arange(len(target_names))
plt.title('Normalized Confusion matrix')
plt.xlabel('Predicted label')
plt.xticks(tick_marks, target_names, rotation=45)
plt.ylabel('True label')
plt.yticks(tick_marks, target_names)
plt.clim(0,1)
plt.colorbar()
mne.viz.tight_layout()
plt.show()
# -

# ## Results
