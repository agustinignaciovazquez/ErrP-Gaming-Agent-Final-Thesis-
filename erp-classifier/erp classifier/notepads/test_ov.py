# %%
#  "import" de las librerías que vamos a estar usando.
import os
import numpy as np
import mne
import pylab
##import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
##from mpl_toolkits.axes_grid1 import make_axes_locatable




def full_extent(ax, pad=0.0):
    """Get the full extent of an axes, including axes labels, tick labels, and
    titles."""
    # For text objects, we need to draw the figure first, otherwise the extents
    # are undefined.
    ax.figure.canvas.draw()
    items = ax.get_xticklabels() + ax.get_yticklabels()
    #    items += [ax, ax.title, ax.xaxis.label, ax.yaxis.label]
    items += [ax, ax.title]
    bbox = Bbox.union([item.get_window_extent() for item in items])

    return bbox.expanded(1.0 + pad, 1.0 + pad)

def savesubfigure(a,filename):
    allaxes = a.get_axes()
    subfig = allaxes[0]

    # Save just the portion _inside_ the second axis's boundaries
    extent = full_extent(subfig).transformed(a.dpi_scale_trans.inverted())

    for item in ([subfig.title, subfig.xaxis.label, subfig.yaxis.label] +
                 subfig.get_xticklabels() + subfig.get_yticklabels()):
        item.set_fontsize(14)

    # Alternatively,
    # extent = ax.get_tightbbox(fig.canvas.renderer).transformed(fig.dpi_scale_trans.inverted())
    a.savefig(filename, bbox_inches=extent)

# versión de MNE, chequear que estamos usando mne3
mne.sys_info()
# Acá leemos un archivo particular
mne.set_log_level("WARNING")

from mne.datasets import sample
data_path = sample.data_path()


raw= mne.io.read_raw_brainvision('C:\\Users\\agust\\Desktop\\pf-agent-training-bw\\erp-classifier\\erp classifier\\data\\subject1\\subject1-1\\record-bv-generic-alex-[2019.06.15-18.43.41].vhdr',
    preload=True,
    eog=('EOG1_1','EOG2_1'),
    misc=('EMG1_1','EMG2_1'),
    verbose=True)
raw.rename_channels(lambda s: s.strip("."))

#raw.set_montage("standard_1020")
#raw.set_eeg_reference("average")

#eeg_mne.filter(1,20)
raw_copy=raw.copy()
print("Hola")
#raw_copy.drop_channels(['C4_1', 'F3_1' , 'F4_1', 'P3_1','P4_1','EOG1_1','EMG2_1'])
##ax = raw.copy.gca()
##ax.set_xticks(numpy.arange(0, 1, 0.5))
##plt.grid()
##raw_copy = make_axes_locatable(plt.gca())
#raw_copy.plot_psd()
#raw.filter(1,20)
#raw.plot_psd()

a = raw_copy.plot()
savesubfigure(a,'kcomplex1.eps')



#a = raw.plot(show_options=True,title='KComplex2',start=504,duration=30,n_channels=10, scalings=dict(eeg=20e-6))
# chequean que la frecuencia de sampleo sea la esperada
print('Sampling Frequency: %d' %  raw.info['sfreq'] )

raw.plot(scalings='auto',n_channels=10,block=True)

print(raw.annotations)

print (raw.annotations.description)

raw.annotations.save("Annotations.txt")