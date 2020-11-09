import time
from random import random as rand
from pylsl import StreamInfo, StreamOutlet
import mne
import numpy as np

EVENTS_IDS = {'Closer': 10001, 'Further': 10002, 'Start': 10003, 'Finish': 10004}
EVENTS_TMIN = 0.0
EVENTS_TMAX = 2.0
montage = ['standard_1020']
file = '../data/subject2/subject2-1/record-bv-generic-gonza-[2019.05.25-14.37.56].vhdr'
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
#sig_mne.filter(l_freq=0.5, h_freq=10)

# Notch filter
#sig_mne.notch_filter(np.arange(50, 100, 50), filter_length='auto', phase='zero')
#sig_mne, events = sig_mne.copy().resample(10, npad='auto', events=events)


epochs = mne.Epochs(sig_mne, events, EVENTS_IDS, tmin=EVENTS_TMIN, tmax=EVENTS_TMAX, baseline=(0, 0),
                    picks=None, preload=True, reject=None, flat=None, proj=False, decim=1,
                    reject_tmin=None, reject_tmax=None, detrend=None, on_missing='error',
                    reject_by_annotation=True, metadata=None, verbose=None)


experiences = []
info = StreamInfo('BrainVision', 'EEG', 8, 250, 'float32', 'bv001')
outlet = StreamOutlet(info)

info_markers = StreamInfo('BrainVision Markers', 'Markers', 1, 0.5, 'int32', 'bv001')
outlet_markers = StreamOutlet(info_markers)

print("now sending data...")
marks_arr = []
epochs_arr = epochs.get_data()[:, :8, 1:]
event_index = 0

epoch_aux = epochs_arr[0]
time.sleep(20)

for epoch in epochs_arr:
    mark = events[event_index][2] % 10
    outlet_markers.push_sample([mark])
    event_index = event_index + 1
    marks_arr.append(mark)
    #time.sleep(0.004)
    for i in range(len(epoch[0])):
        ch_values = [epoch[0][i], epoch[1][i], epoch[2][i], epoch[3][i], epoch[4][i], epoch[5][i], epoch[6][i], epoch[7][i]]
        outlet.push_sample(ch_values)
        time.sleep(0.004)

for i in range(len(epoch_aux[0])):
    ch_values = [epoch_aux[0][i], epoch_aux[1][i], epoch_aux[2][i], epoch_aux[3][i], epoch_aux[4][i], epoch_aux[5][i], epoch_aux[6][i], epoch_aux[7][i]]
    outlet.push_sample(ch_values)
    time.sleep(0.004)
for i in range(len(epoch_aux[0])):
    ch_values = [epoch_aux[0][i], epoch_aux[1][i], epoch_aux[2][i], epoch_aux[3][i], epoch_aux[4][i], epoch_aux[5][i], epoch_aux[6][i], epoch_aux[7][i]]
    outlet.push_sample(ch_values)
    time.sleep(0.004)
print(marks_arr)